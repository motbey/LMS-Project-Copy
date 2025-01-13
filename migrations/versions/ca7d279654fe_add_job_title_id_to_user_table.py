"""Add job_title_id to User table

Revision ID: ca7d279654fe
Revises: 238d9e8d6453
Create Date: 2025-01-13 09:08:47.920159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca7d279654fe'
down_revision = '238d9e8d6453'
branch_labels = None
depends_on = None


def upgrade():
    # ### Directly adjust the user table ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_title_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_job_title', 'job_title', ['job_title_id'], ['id'])
        batch_op.create_foreign_key('fk_user_company', 'company', ['company_id'], ['id'])

    # Adjust the job_title table
    with op.batch_alter_table('job_title', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_job_title_name', ['name'])

    # Optional: Clean up old structures or add additional changes here as needed
    # Avoid dropping any `_alembic_tmp_module` or redundant structures
    pass


def downgrade():
    # ### Revert changes to the user table ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_job_title', type_='foreignkey')
        batch_op.drop_constraint('fk_user_company', type_='foreignkey')
        batch_op.drop_column('job_title_id')

    # Revert changes to the job_title table
    with op.batch_alter_table('job_title', schema=None) as batch_op:
        batch_op.drop_constraint('uq_job_title_name', type_='unique')

    # Optional: Recreate dropped structures if necessary
    pass
