from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '08964fc0441f'
down_revision = 'd66344d1050f'  # Ensure this matches the previous migration
branch_labels = None
depends_on = None

def upgrade():
    # Drop the user_old table if it exists (to handle leftover tables from previous issues)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'user_old' in inspector.get_table_names():
        op.execute('DROP TABLE user_old')

    # Rename 'user' table to 'user_old' and create a new 'user' table
    op.rename_table('user', 'user_old')
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('company_id', sa.Integer, sa.ForeignKey('company.id')),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
    )

    # Create the new location table
    op.create_table(
        'location',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

    # Add the Module table for SCORM handling
    op.create_table(
        'module',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('status', sa.String(50), nullable=False)
    )


def downgrade():
    # Drop the new tables
    op.drop_table('module')
    op.drop_table('location')
    op.drop_table('user')

    # Restore the old user table
    op.rename_table('user_old', 'user')
