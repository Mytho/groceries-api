"""create user table

Revision ID: bb124c0db57
Revises:
Create Date: 2015-04-29 16:47:08.983040

"""

# revision identifiers, used by Alembic.
revision = 'bb124c0db57'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(64), nullable=False, unique=True),
            sa.Column('password', sa.String(64), nullable=False))


def downgrade():
    op.drop_table('user')
