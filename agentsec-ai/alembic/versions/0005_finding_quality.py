"""Add normalized finding quality and analyst workflow fields."""

from alembic import op
import sqlalchemy as sa

revision = "0005_finding_quality"
down_revision = "0004_approved_targets"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = (
        ("source_tool", sa.String(100)),
        ("category", sa.String(100)),
        ("confidence", sa.Float()),
        ("asset", sa.Text()),
        ("parameter", sa.String(255)),
        ("remediation", sa.Text()),
        ("cwe", sa.String(50)),
        ("owasp_category", sa.String(100)),
        ("verification_state", sa.String(30), "unverified"),
        ("analyst_notes", sa.Text()),
        ("assignee", sa.String(255)),
        ("due_date", sa.DateTime(timezone=True)),
        ("risk_acceptance", sa.Boolean(), False),
        ("dedup_key", sa.String(64)),
    )
    for item in columns:
        name, type_ = item[:2]
        kwargs = {"nullable": True}
        if len(item) == 3:
            kwargs["server_default"] = sa.text(f"'{item[2]}'" if isinstance(item[2], str) else "false")
        op.add_column("active_findings", sa.Column(name, type_, **kwargs))
    op.execute(
        "UPDATE active_findings SET dedup_key = md5(lower(trim(title)) || chr(31) || "
        "lower(trim(coalesce(affected_url, ''))) || ':' || id::text) WHERE dedup_key IS NULL"
    )
    op.alter_column("active_findings", "dedup_key", nullable=False)
    op.create_index("ix_active_findings_dedup_key", "active_findings", ["dedup_key"])


def downgrade() -> None:
    op.drop_index("ix_active_findings_dedup_key", table_name="active_findings")
    for name in (
        "dedup_key", "risk_acceptance", "due_date", "assignee", "analyst_notes",
        "verification_state", "owasp_category", "cwe", "remediation", "parameter",
        "asset", "confidence", "category", "source_tool",
    ):
        op.drop_column("active_findings", name)
