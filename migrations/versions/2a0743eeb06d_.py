"""empty message

Revision ID: 2a0743eeb06d
Revises: 
Create Date: 2020-04-26 19:27:30.092801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a0743eeb06d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('creation_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modification_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('remove_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    role_table = op.create_table('role',
    sa.Column('name', sa.Enum('ADMIN', 'USER', name='rolename'), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('record',
    sa.Column('product_id', sa.String(length=40), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'date')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('creation_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modification_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('remove_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'USER', name='rolename'), nullable=True),
    sa.ForeignKeyConstraint(['role'], ['role.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', 'remove_date', name='unique_user_email')
    )
    op.create_table('user_to_product',
    sa.Column('product_id', sa.String(length=40), nullable=False),
    sa.Column('user_id', sa.String(length=250), nullable=False),
    sa.Column('difference_trigger', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'user_id'),
    sa.UniqueConstraint('user_id', 'product_id', name='_email_product_uc')
    )
    # ### end Alembic commands ###
    op.bulk_insert(
        role_table,
        [
            {'name': 'ADMIN'},
            {'name': 'USER'}
        ]
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_to_product')
    op.drop_table('user')
    op.drop_table('record')
    op.drop_table('role')
    op.drop_table('product')
    # ### end Alembic commands ###
