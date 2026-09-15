"""add username to users

Revision ID: 9a4c7e2f1b30
Revises: 5e270031d284
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "9a4c7e2f1b30"
down_revision: Union[str, None] = "5e270031d284"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=100), nullable=True))
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_column("users", "username")
