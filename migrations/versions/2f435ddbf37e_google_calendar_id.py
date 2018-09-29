"""google calendar id

Revision ID: 2f435ddbf37e
Revises: 1051a5fd6a75
Create Date: 2018-09-23 18:31:21.953390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f435ddbf37e'
down_revision = '1051a5fd6a75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultation', sa.Column('google_event_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('consultation', 'google_event_id')
    # ### end Alembic commands ###