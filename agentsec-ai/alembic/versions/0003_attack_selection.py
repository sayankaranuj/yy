"""Add explicit attack selection to active scans."""

from alembic import op
import sqlalchemy as sa

revision = "0003_attack_selection"
down_revision = "0002_active_api_storage"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add nullable selector configuration for backward compatibility."""

    op.add_column(
        "active_scans",
        sa.Column("selected_attack_categories", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    """Remove selector configuration."""

    op.drop_column("active_scans", "selected_attack_categories")
