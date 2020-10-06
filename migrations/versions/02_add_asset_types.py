"""empty message

Revision ID: 02_add_asset_types
Revises: 01_healthz_table

"""
from alembic import op
import sqlalchemy as sa
import azure_ingester_api.api.models as m


# revision identifiers, used by Alembic.
revision = '02_add_asset_types'
down_revision = '01_healthz_table'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'asset_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(250), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    m.insert_data_from_csv('migrations/data/asset_type_v1.csv', m.DataAssetType.__table__, op.get_bind())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('asset_type')
    # ### end Alembic commands ###``