"""db migration

Revision ID: 373a21295ab
Revises: 21f5b2d3905d
Create Date: 2015-05-05 15:42:33.474470

"""

# revision identifiers, used by Alembic.
revision = '373a21295ab'
down_revision = '21f5b2d3905d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('items')
    items = op.create_table('items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('is_bought', sa.Boolean, default=False, nullable=False),
        sa.Column('created', sa.DateTime, default=sa.func.now(),
                  nullable=False),
        sa.Column('modified', sa.DateTime, default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False))


def downgrade():
    op.drop_table('items')
    op.create_table('items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('is_bought', sa.Boolean, default=False, nullable=False),
        sa.Column('modified', sa.DateTime, default=sa.func.now(),
                  onupdate=sa.func.now(), nullable=False),
        sa.Column('created', sa.DateTime, default=sa.func.now()))
