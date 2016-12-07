"""create vehicle_positions table

Revision ID: 2aa1874dd408
Revises: 5d1515733a63
Create Date: 2016-12-06 21:32:06.944994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aa1874dd408'
down_revision = '5d1515733a63'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vehicle_positions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('type', sa.String(128), nullable=False),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('vehicle_id', sa.String(128), nullable=False)
    )


def downgrade():
    op.drop_table('vehicle_positions')
