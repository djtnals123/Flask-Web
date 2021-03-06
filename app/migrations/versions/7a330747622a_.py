"""empty message

Revision ID: 7a330747622a
Revises: 
Create Date: 2021-12-02 05:02:01.058953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a330747622a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('hospital', sa.String(length=1), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('auth',
    sa.Column('id', sa.String(length=30), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id', 'role')
    )
    op.create_table('board',
    sa.Column('board_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('writer', sa.String(length=30), nullable=False),
    sa.Column('attachment', sa.String(length=87), nullable=True),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['writer'], ['account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('board_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board')
    op.drop_table('auth')
    op.drop_table('account')
    # ### end Alembic commands ###
