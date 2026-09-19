"""Create initial tables

Revision ID: 7abf53cff6e6
Revises: 
Create Date: 2026-09-19 13:02:40.903475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7abf53cff6e6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'identities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('full_name', sa.Text(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uni_identities_email')
    )

    op.create_table(
        'credentials',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('identity_id', sa.Integer(), nullable=False),
        sa.Column('provider', sa.Text(), nullable=False),
        sa.Column('provider_user_id', sa.Text(), nullable=True),
        sa.Column('email', sa.Text(), nullable=True),
        sa.Column('password_hash', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(
            ['identity_id'], ['identities.id'],
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'articles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('slug', sa.Text(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Text(), server_default="draft", nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['author_id'], ['identities.id'],
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title', name='unique_tags_title')
    )

    op.create_table(
        'article_tags',
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('article_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['article_id'], ['articles.id'],
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['tag_id'], ['tags.id'],
            onupdate='CASCADE', ondelete='CASCADE'
        )
    )


def downgrade() -> None:
    op.drop_table('article_tags')
    op.drop_table('tags')
    op.drop_table('articles')
    op.drop_table('credentials')
    op.drop_table('identities')