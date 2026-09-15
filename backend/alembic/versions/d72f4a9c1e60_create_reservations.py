"""create reservations

Revision ID: d72f4a9c1e60
Revises: a62e8b4d7c19
"""
from alembic import op
import sqlalchemy as sa

revision = "d72f4a9c1e60"
down_revision = "a62e8b4d7c19"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("reservations",
        sa.Column("booking_id", sa.String(30), nullable=False),
        sa.Column("guest_id", sa.String(), nullable=False),
        sa.Column("room_id", sa.String(), nullable=False),
        sa.Column("check_in", sa.Date(), nullable=False),
        sa.Column("check_out", sa.Date(), nullable=False),
        sa.Column("adults", sa.Integer(), nullable=False),
        sa.Column("children", sa.Integer(), nullable=False),
        sa.Column("special_request", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["guest_id"], ["guests.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reservations_booking_id", "reservations", ["booking_id"], unique=True)
    op.create_index("ix_reservations_guest_id", "reservations", ["guest_id"])
    op.create_index("ix_reservations_room_id", "reservations", ["room_id"])


def downgrade():
    op.drop_table("reservations")
