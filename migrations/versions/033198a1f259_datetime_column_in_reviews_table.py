"""datetime column in reviews table

Revision ID: 033198a1f259
Revises: b848199f5eb9
Create Date: 2018-12-04 22:05:22.332159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '033198a1f259'
down_revision = 'b848199f5eb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('pub_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('review', 'pub_date')
    # ### end Alembic commands ###
