"""seed example user"""
from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def upgrade():
    hashed_password = pwd_context.hash("password123")
    op.execute(
        f"INSERT INTO users (name, email, password) VALUES ('Example User', 'user@example.com', '{hashed_password}')"
    )

def downgrade():
    op.execute("DELETE FROM users WHERE email='user@example.com'")