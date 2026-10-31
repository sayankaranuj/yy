"""Add administrator-approved target allowlist."""

from alembic import op
import sqlalchemy as sa

revision = "0004_approved_targets"
down_revision = "0003_attack_selection"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "approved_targets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("target", sa.String(length=255), nullable=False),
        sa.Column("approved_by", sa.String(length=255), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("target"),
    )
    op.create_index("ix_approved_targets_target", "approved_targets", ["target"])


def downgrade() -> None:
    op.drop_index("ix_approved_targets_target", table_name="approved_targets")
    op.drop_table("approved_targets")
