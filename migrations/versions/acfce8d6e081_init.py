"""Init

Revision ID: acfce8d6e081
Revises: 
Create Date: 2023-09-07 00:37:41.827269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acfce8d6e081'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=200), nullable=True),
    sa.Column('last_name', sa.String(length=200), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('role', sa.Enum('approver', 'complainer', 'admin', name='roletype'), server_default='complainer', nullable=False),
    sa.Column('iban', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('complaints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('photo_url', sa.String(length=200), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('utcnow()'), nullable=True),
    sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='state'), server_default='pending', nullable=False),
    sa.Column('complainer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['complainer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('complaints')
    op.drop_table('users')
    # ### end Alembic commands ###
