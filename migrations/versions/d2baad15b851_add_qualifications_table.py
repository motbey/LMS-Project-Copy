"""Add qualifications table

Revision ID: d2baad15b851
Revises: 47401df42c46
Create Date: 2025-01-06 12:40:48.380447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2baad15b851'
down_revision = '47401df42c46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('qualification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('valid_days', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.TEXT(),
               type_=sa.String(length=10),
               nullable=False,
               existing_server_default=sa.text("'Active'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=10),
               type_=sa.TEXT(),
               nullable=True,
               existing_server_default=sa.text("'Active'"))

    op.drop_table('qualification')
    # ### end Alembic commands ###
