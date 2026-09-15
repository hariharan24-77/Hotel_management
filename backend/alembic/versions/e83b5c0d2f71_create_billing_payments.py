"""create billing and payments
Revision ID: e83b5c0d2f71
Revises: d72f4a9c1e60
"""
from alembic import op
import sqlalchemy as sa
revision="e83b5c0d2f71"; down_revision="d72f4a9c1e60"; branch_labels=None; depends_on=None
def base_columns():
    return [sa.Column("id",sa.String(),nullable=False),sa.Column("created_at",sa.DateTime(),nullable=False),sa.Column("updated_at",sa.DateTime(),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False),sa.Column("is_deleted",sa.Boolean(),nullable=False)]
def upgrade():
    op.create_table("invoices",sa.Column("invoice_no",sa.String(40),nullable=False),sa.Column("reservation_id",sa.String(),nullable=False),sa.Column("room_charge",sa.Numeric(12,2),nullable=False),sa.Column("service_charge",sa.Numeric(12,2),nullable=False),sa.Column("tax",sa.Numeric(12,2),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("paid_amount",sa.Numeric(12,2),nullable=False),sa.Column("payment_status",sa.String(20),nullable=False),*base_columns(),sa.ForeignKeyConstraint(["reservation_id"],["reservations.id"]),sa.PrimaryKeyConstraint("id"),sa.UniqueConstraint("reservation_id"))
    op.create_index("ix_invoices_invoice_no","invoices",["invoice_no"],unique=True); op.create_index("ix_invoices_reservation_id","invoices",["reservation_id"],unique=True)
    op.create_table("payments",sa.Column("payment_no",sa.String(40),nullable=False),sa.Column("bill_id",sa.String(),nullable=False),sa.Column("amount",sa.Numeric(12,2),nullable=False),sa.Column("payment_method",sa.String(20),nullable=False),*base_columns(),sa.ForeignKeyConstraint(["bill_id"],["invoices.id"]),sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_payments_payment_no","payments",["payment_no"],unique=True); op.create_index("ix_payments_bill_id","payments",["bill_id"])
def downgrade(): op.drop_table("payments"); op.drop_table("invoices")
