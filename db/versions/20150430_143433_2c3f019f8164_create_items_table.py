"""create items table

Revision ID: 2c3f019f8164
Revises: bb124c0db57
Create Date: 2015-04-30 14:34:33.785558

"""

# revision identifiers, used by Alembic.
revision = '2c3f019f8164'
down_revision = 'bb124c0db57'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('is_bought', sa.Boolean, default=False, nullable=False),
        sa.Column('modified', sa.DateTime, default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False))


def downgrade():
    op.drop_table('items')
