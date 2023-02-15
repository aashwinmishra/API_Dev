"""Set username and short desc to not nullable

Revision ID: 454657acae27
Revises: 5477f04cb4e1
Create Date: 2023-02-10 18:45:01.633363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '454657acae27'
down_revision = '5477f04cb4e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("user", "username", nullable=False)
    op.alter_column("user", "short_description", nullable=False)


def downgrade() -> None:
    op.drop_column("user", "test")
    op.alter_column("user", "username", nullable=True)


