"""create guests

Revision ID: a62e8b4d7c19
Revises: f51a9d3c6b42
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "a62e8b4d7c19"
down_revision: Union[str, None] = "f51a9d3c6b42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("guests",
        sa.Column("name", sa.String(100), nullable=False), sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("email", sa.String(150), nullable=False), sa.Column("gender", sa.String(30), nullable=False),
        sa.Column("dob", sa.Date(), nullable=False), sa.Column("address", sa.Text(), nullable=False),
        sa.Column("id_proof_type", sa.String(50), nullable=False), sa.Column("id_proof_number", sa.String(100), nullable=False),
        sa.Column("id", sa.String(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_guests_name"), "guests", ["name"], unique=False)
    op.create_index(op.f("ix_guests_id_proof_number"), "guests", ["id_proof_number"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_guests_id_proof_number"), table_name="guests")
    op.drop_index(op.f("ix_guests_name"), table_name="guests")
    op.drop_table("guests")
