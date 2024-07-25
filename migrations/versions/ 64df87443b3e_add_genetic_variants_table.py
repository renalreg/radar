"""add_genetic_variants_table

Revision ID: 64df87443b3e
Revises: 46944ada7c1f
Create Date: 2024-07-10 14:14:57.640960

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM

# revision identifiers, used by Alembic.
revision = '64df87443b3e'
down_revision = '46944ada7c1f'
branch_labels = None
depends_on = None

# Create lookup enums
genome_build = ENUM('hg38', 'hg19', 'hg18', name='genome_build')
zygosity_enum = ENUM('homozygous', 'heterozygous', 'hemizygous', name='zygosity_enum')
phase_enum = ENUM('cis', 'trans', 'NA', name='phase_enum')
rna_effect_enum = ENUM('splicing', 'not splicing', 'not tested', name='rna_effect_enum')
interpretation_enum = ENUM('0', '1', '2', '3', '4', '5', name='interpretation_enum')

def upgrade():


    # Create genetic_variants table
    op.create_table(
        'genetic_variants',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('genetics_id', UUID(as_uuid=True), sa.ForeignKey('genetics.id', ondelete='CASCADE'), nullable=False),
        sa.Column('gene_panel_tested_id', sa.String, nullable=True),
        sa.Column('gen_build', genome_build, server_default='hg38'),
        sa.Column('chromosome', sa.Integer, nullable=True),
        sa.Column('start_pos', sa.Integer, nullable=True),
        sa.Column('stop_pos', sa.Integer, nullable=True),
        sa.Column('ref_allele', sa.String, nullable=True),
        sa.Column('variant_allele', sa.String, nullable=True),
        sa.Column('gene_symbol', sa.String, nullable=True),
        sa.Column('ref_seq', sa.String, nullable=True),
        sa.Column('cdna_pos', sa.String, nullable=True),
        sa.Column('protein_residue', sa.Integer, nullable=True),
        sa.Column('ref_amino', sa.String, nullable=True),
        sa.Column('variant_amino', sa.String, nullable=True),
        sa.Column('zygosity', zygosity_enum, nullable=True),
        sa.Column('phase', phase_enum, server_default='NA'),
        sa.Column('rna_effect', rna_effect_enum, server_default='not tested'),
        sa.Column('interpretation', interpretation_enum, nullable=True),
        sa.Column('other_details', sa.String, nullable=True)
    )



def downgrade():
    op.drop_table("genetic_variants")

    # Drop the enums
    interpretation_enum.drop(op.get_bind())
    rna_effect_enum.drop(op.get_bind())
    phase_enum.drop(op.get_bind())
    zygosity_enum.drop(op.get_bind())
    genome_build.drop(op.get_bind())

