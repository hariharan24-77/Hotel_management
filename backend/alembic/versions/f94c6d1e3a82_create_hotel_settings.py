"""create hotel settings
Revision ID: f94c6d1e3a82
Revises: e83b5c0d2f71
"""
from alembic import op
import sqlalchemy as sa
revision="f94c6d1e3a82";down_revision="e83b5c0d2f71";branch_labels=None;depends_on=None
def upgrade():
    op.create_table("hotel_settings",sa.Column("name",sa.String(150),nullable=False),sa.Column("phone",sa.String(20),nullable=False),sa.Column("email",sa.String(150),nullable=False),sa.Column("address",sa.Text(),nullable=False),sa.Column("gst",sa.Numeric(5,2),nullable=False),sa.Column("service_tax",sa.Numeric(5,2),nullable=False),sa.Column("cash",sa.Boolean(),nullable=False),sa.Column("upi",sa.Boolean(),nullable=False),sa.Column("card",sa.Boolean(),nullable=False),sa.Column("id",sa.String(),nullable=False),sa.Column("created_at",sa.DateTime(),nullable=False),sa.Column("updated_at",sa.DateTime(),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False),sa.Column("is_deleted",sa.Boolean(),nullable=False),sa.PrimaryKeyConstraint("id"))
def downgrade():op.drop_table("hotel_settings")
