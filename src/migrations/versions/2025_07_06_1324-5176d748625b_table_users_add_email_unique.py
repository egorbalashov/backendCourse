"""table users add email unique

Revision ID: 5176d748625b
Revises: 8fa2c135e91b
Create Date: 2025-07-06 13:24:24.290843

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5176d748625b"
down_revision: Union[str, Sequence[str], None] = "8fa2c135e91b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
