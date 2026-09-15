"""create room types

Revision ID: c34d7a1e820f
Revises: 9a4c7e2f1b30
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c34d7a1e820f"
down_revision: Union[str, None] = "9a4c7e2f1b30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "room_types",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("base_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("bed_type", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_room_types_name"), "room_types", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_room_types_name"), table_name="room_types")
    op.drop_table("room_types")
