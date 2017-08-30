"""empty message

Revision ID: 213a9685bf84
Revises: 
Create Date: 2017-08-30 18:39:48.488575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '213a9685bf84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=300), nullable=False),
    sa.Column('user_password', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('bucket_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_name', sa.String(length=300), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('bucket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bucket_id'], ['bucket_list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activities')
    op.drop_table('bucket_list')
    op.drop_table('user')
    # ### end Alembic commands ###
