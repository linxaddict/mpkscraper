"""added new models for stops

Revision ID: 44516a7495c7
Revises: 79c98cc7dabc
Create Date: 2016-12-15 23:32:14.681300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44516a7495c7'
down_revision = '79c98cc7dabc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stops',
        sa.Column('id', sa.String(128), primary_key=True),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('type', sa.String(16), nullable=False),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('longitude', sa.Float, nullable=False)
    )

    op.create_table(
        'line_stops',
        sa.Column('id', sa.String(128), primary_key=True),
        sa.Column('line', sa.String(128), nullable=False)
    )


def downgrade():
    op.drop_table('stops')
    op.drop_table('line_stops')
