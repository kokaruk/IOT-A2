"""referral medical certificate

Revision ID: 1051a5fd6a75
Revises: 9d7d47019724
Create Date: 2018-09-22 15:09:21.598313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1051a5fd6a75'
down_revision = '9d7d47019724'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medical_certificate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('consultation_details_id', sa.Integer(), nullable=False),
    sa.Column('certificate', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['consultation_details_id'], ['consultation_details.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('referral',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('consultation_details_id', sa.Integer(), nullable=False),
    sa.Column('procedure_name', sa.String(length=120), nullable=True),
    sa.Column('referred_practitioner', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['consultation_details_id'], ['consultation_details.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('condition', sa.Column('consultation_details_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'condition', 'consultation_details', ['consultation_details_id'], ['id'])
    op.add_column('medication', sa.Column('consultation_details_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'medication', 'consultation_details', ['consultation_details_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'medication', type_='foreignkey')
    op.drop_column('medication', 'consultation_details_id')
    op.drop_constraint(None, 'condition', type_='foreignkey')
    op.drop_column('condition', 'consultation_details_id')
    op.drop_table('referral')
    op.drop_table('medical_certificate')
    # ### end Alembic commands ###