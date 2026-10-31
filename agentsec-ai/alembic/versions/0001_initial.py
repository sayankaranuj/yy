"""Initial migration — create all tables from SQLAlchemy metadata.

Revision ID: 0001_initial
Revises: 
Create Date: 2026-07-30 00:00:00.000000
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables from SQLAlchemy metadata."""
    # Importing here to ensure app settings are available
    from backend.models.base import Base
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    """Drop all tables created in upgrade."""
    from backend.models.base import Base
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
