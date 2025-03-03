"""Add PlayerStats model

Revision ID: manual_add_playerstats
Revises: 1611794bd5b8
Create Date: 2025-03-03 18:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'manual_add_playerstats'
down_revision = '1611794bd5b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player_stats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.Column('tournament_id', sa.Integer(), nullable=False),
        sa.Column('matches_played', sa.Integer(), nullable=True),
        sa.Column('minutes_played', sa.Integer(), nullable=True),
        sa.Column('goals', sa.Integer(), nullable=True),
        sa.Column('assists', sa.Integer(), nullable=True),
        sa.Column('penalty_goals', sa.Integer(), nullable=True),
        sa.Column('own_goals', sa.Integer(), nullable=True),
        sa.Column('yellow_cards', sa.Integer(), nullable=True),
        sa.Column('red_cards', sa.Integer(), nullable=True),
        sa.Column('goals_per_match', sa.Float(), nullable=True),
        sa.Column('minutes_per_goal', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_stats_id'), 'player_stats', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_player_stats_id'), table_name='player_stats')
    op.drop_table('player_stats')
    # ### end Alembic commands ### 