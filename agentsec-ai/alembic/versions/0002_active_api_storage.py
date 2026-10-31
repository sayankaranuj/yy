"""Add integer-keyed tables used by the active API and workflow store."""

from alembic import op

revision = "0002_active_api_storage"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from backend.models.active_api import (
        ActiveFinding,
        ActiveScan,
        ActiveWorkflow,
        ActiveWorkflowResult,
        ActiveWorkflowTask,
    )
    bind = op.get_bind()
    for model in (ActiveScan, ActiveFinding, ActiveWorkflow, ActiveWorkflowTask, ActiveWorkflowResult):
        model.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    from backend.models.active_api import (
        ActiveFinding,
        ActiveScan,
        ActiveWorkflow,
        ActiveWorkflowResult,
        ActiveWorkflowTask,
    )
    bind = op.get_bind()
    for model in (ActiveWorkflowResult, ActiveWorkflowTask, ActiveWorkflow, ActiveFinding, ActiveScan):
        model.__table__.drop(bind=bind, checkfirst=True)
