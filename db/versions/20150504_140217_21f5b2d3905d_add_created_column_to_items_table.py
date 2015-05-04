"""add created column to items table

Revision ID: 21f5b2d3905d
Revises: 2c3f019f8164
Create Date: 2015-05-04 14:02:17.618279

"""

# revision identifiers, used by Alembic.
revision = '21f5b2d3905d'
down_revision = '2c3f019f8164'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('items',
        sa.Column('created', sa.DateTime, default=sa.func.now()))


def downgrade():
    op.drop_column('items', 'created')
