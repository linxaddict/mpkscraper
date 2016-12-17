"""added foreign key to the line_stops

Revision ID: 48e2185b4a81
Revises: 44516a7495c7
Create Date: 2016-12-17 21:50:48.779742

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '48e2185b4a81'
down_revision = '44516a7495c7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('fk_stop_line_stop', 'line_stops', 'stops', ['line_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_stop_line_stop', 'stops')
