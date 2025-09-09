"""add learning_path and progress columns to users table"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    # Add learning_path and progress columns to users table
    op.add_column('users', sa.Column('learning_path', sa.String(), nullable=True))
    op.add_column('users', sa.Column('progress', sa.String(), nullable=True))

def downgrade():
    # Remove learning_path and progress columns from users table
    op.drop_column('users', 'progress')
    op.drop_column('users', 'learning_path')