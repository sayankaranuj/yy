from datetime import datetime, timedelta, timezone

import pytest

from backend.workers.recovery import StaleTaskRecoveryService


class FakeRepository:
    def __init__(self, attempts):
        self.attempts = attempts
        self.updated = []

    async def list_stale_task_attempts(self, cutoff, scan_id=None):
        return list(self.attempts)

    async def recover_task_attempt(self, attempt_id, **kwargs):
        attempt = next(item for item in self.attempts if item["id"] == attempt_id)
        attempt = {**attempt, **kwargs, "status": "dead_lettered" if kwargs["dead_letter"] else "retrying"}
        self.updated.append(attempt)
        return attempt


@pytest.mark.asyncio
async def test_stale_attempt_is_retried_with_recovery_metadata():
    attempts = [{
        "id": 4, "attempt_number": 1, "task_name": "workers.recon.run",
        "workflow_scan_id": 12, "queue": "recon_queue",
    }]
    queued = []
    service = StaleTaskRecoveryService(FakeRepository(attempts), enqueue=lambda *args, **kwargs: queued.append((args, kwargs)))

    result = await service.recover(stale_after=timedelta(minutes=5), now=datetime.now(timezone.utc))

    assert result[0]["status"] == "retrying"
    assert queued[0][1]["queue"] == "recon_queue"
    assert queued[0][1]["headers"]["recovered_from_attempt"] == 4


@pytest.mark.asyncio
async def test_attempt_limit_routes_stale_attempt_to_dead_letter_queue():
    attempts = [{
        "id": 9, "attempt_number": 3, "task_name": "workers.recon.run",
        "workflow_scan_id": 12, "queue": "recon_queue",
    }]
    queued = []
    repository = FakeRepository(attempts)
    service = StaleTaskRecoveryService(repository, max_attempts=3, enqueue=lambda *a, **k: queued.append(k))

    result = await service.recover(stale_after=timedelta(minutes=5))

    assert result[0]["status"] == "dead_lettered"
    assert result[0]["queue"] == "workflow_dead_letter_queue"
    assert queued == []
