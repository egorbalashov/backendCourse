"""add bookings

Revision ID: 448e61058ef0
Revises: 5176d748625b
Create Date: 2025-07-16 12:13:14.878797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "448e61058ef0"
down_revision: Union[str, Sequence[str], None] = "5176d748625b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fk_booking_room_id", sa.Integer(), nullable=False),
        sa.Column("fk_booking_user_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["fk_booking_room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["fk_booking_user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("bookings")
