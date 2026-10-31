import asyncio

from backend.core.eventbus import EventBus
from backend.core.state_machine import StateMachine
from backend.core.decision_engine import DecisionEngine
from backend.core.fallback import FallbackManager


def _ensure_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def test_eventbus_publish_subscribe():
    eb = EventBus()
    results = []

    async def handler(event, payload):
        results.append((event, payload))

    eb.subscribe("scan.complete", handler)
    eb.publish("scan.complete", {"id": 1})

    # allow the event loop to schedule tasks
    loop = _ensure_event_loop()
    loop.run_until_complete(asyncio.sleep(0.05))

    assert results == [("scan.complete", {"id": 1})]


def test_state_machine_transitions():
    sm = StateMachine("pending")
    called = {"flag": False}

    def on_start():
        called["flag"] = True

    sm.add_transition("pending", "running", on_start)
    sm.trigger("running")
    assert sm.state == "running"
    assert called["flag"]


def test_decision_engine_rules():
    de = DecisionEngine()

    def high_priority(ctx):
        return ctx.get("severity") == "high"

    de.register_rule(high_priority)
    matched = de.evaluate({"severity": "high"})
    assert len(matched) == 1


def test_fallback_manager_retries():
    fm = FallbackManager(retries=2, backoff=0)

    async def flaky(x):
        if x < 2:
            raise ValueError("fail")
        return "ok"

    async def run():
        return await fm.run_with_retry(flaky, 2)

    res = _ensure_event_loop().run_until_complete(run())
    assert res == "ok"
