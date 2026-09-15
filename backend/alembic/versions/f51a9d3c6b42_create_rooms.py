"""create rooms

Revision ID: f51a9d3c6b42
Revises: c34d7a1e820f
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "f51a9d3c6b42"
down_revision: Union[str, None] = "c34d7a1e820f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("room_number", sa.String(length=30), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=False),
        sa.Column("room_type_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["room_type_id"], ["room_types.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rooms_room_number"), "rooms", ["room_number"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_rooms_room_number"), table_name="rooms")
    op.drop_table("rooms")
