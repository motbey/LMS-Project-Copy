"""Sync database state and SCORM module table

Revision ID: 3770235cef63
Revises: 80d78214881e
Create Date: 2025-01-10 17:07:40.508234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3770235cef63'
down_revision = '80d78214881e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('first_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.TEXT(),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('code',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               nullable=False,
               existing_server_default=sa.text("'User'"))
        batch_op.alter_column('status',
               existing_type=sa.TEXT(),
               type_=sa.String(length=10),
               nullable=False,
               existing_server_default=sa.text("'Active'"))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'company', ['company_id'], ['id'])
        batch_op.drop_column('company')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('company', sa.TEXT(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'company', ['company_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('status',
               existing_type=sa.String(length=10),
               type_=sa.TEXT(),
               nullable=True,
               existing_server_default=sa.text("'Active'"))
        batch_op.alter_column('role',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               nullable=True,
               existing_server_default=sa.text("'User'"))
        batch_op.alter_column('code',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.String(length=200),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    # ### end Alembic commands ###
