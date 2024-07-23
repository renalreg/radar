"""add_genetic_variants_table

Revision ID: 64df87443b3e
Revises: 46944ada7c1f
Create Date: 2024-07-10 14:14:57.640960

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '64df87443b3e'
down_revision = '46944ada7c1f'
branch_labels = None
depends_on = None

def upgrade():
    # Create lookup tables
    op.create_table(
        'genetic_variant_genome_builds',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('build', sa.String(10), unique=True, nullable=False)
    )
    op.bulk_insert(
        sa.table('genetic_variant_genome_builds', sa.column('build')),
        [{'build': 'hg38'}, {'build': 'hg19'}, {'build': 'hg18'}]
    )

    op.create_table(
        'genetic_variant_zygosity',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('zygosity', sa.String(20), unique=True, nullable=False)
    )
    op.bulk_insert(
        sa.table('genetic_variant_zygosity', sa.column('zygosity')),
        [{'zygosity': 'homozygous'}, {'zygosity': 'heterozygous'}, {'zygosity': 'hemizygous'}]
    )

    op.create_table(
        'genetic_variant_phase',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('phase', sa.String(10), unique=True, nullable=False)
    )
    op.bulk_insert(
        sa.table('genetic_variant_phase', sa.column('phase')),
        [{'phase': 'cis'}, {'phase': 'trans'}, {'phase': 'NA'}]
    )

    op.create_table(
        'genetic_variant_rna_effect',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('rna_effect', sa.String(20), unique=True, nullable=False)
    )
    op.bulk_insert(
        sa.table('genetic_variant_rna_effect', sa.column('rna_effect')),
        [{'rna_effect': 'splicing'}, {'rna_effect': 'not splicing'}, {'rna_effect': 'not tested'}]
    )

    op.create_table(
        'genetic_variant_interpretation',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('interpretation', sa.Integer, nullable=False)
    )

    op.bulk_insert(
        sa.table('genetic_variant_interpretation', sa.column('interpretation')),
        [{'interpretation': 0}, {'interpretation': 1}, {'interpretation': 2},{'interpretation': 3},{'interpretation': 4},{'interpretation': 5}]
    )

    # Create genetic_variants table
    op.create_table(
        'genetic_variants',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('genetics_id', UUID(as_uuid=True), sa.ForeignKey('genetics.id', ondelete='CASCADE'), nullable=False),
        sa.Column('gene_panel_tested_id', sa.String, nullable=True),
        sa.Column('gen_build', sa.Integer, sa.ForeignKey('genetic_variant_genome_builds.id', ondelete='RESTRICT'), nullable=True, server_default='1'),
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
        sa.Column('zygosity', sa.Integer, sa.ForeignKey('genetic_variant_zygosity.id', ondelete='RESTRICT'), nullable=True),
        sa.Column('phase', sa.Integer, sa.ForeignKey('genetic_variant_phase.id', ondelete='RESTRICT'), nullable=True, server_default='3'),
        sa.Column('rna_effect', sa.Integer, sa.ForeignKey('genetic_variant_rna_effect.id', ondelete='RESTRICT'), nullable=True, server_default='3'),
        sa.Column('interpretation', sa.Integer, sa.ForeignKey('genetic_variant_interpretation.id', ondelete='RESTRICT'), nullable=True),
        sa.Column('other_details', sa.String, nullable=True)
    )



def downgrade():
    op.drop_table("genetic_variants")

    # Drop the genetic_variant_interpretation table
    op.drop_table('genetic_variant_interpretation')

    # Drop the genetic_variant_rna_effect table
    op.drop_table('genetic_variant_rna_effect')

    # Drop the genetic_variant_phase table
    op.drop_table('genetic_variant_phase')

    # Drop the genetic_variant_zygosity table
    op.drop_table('genetic_variant_zygosity')

    # Drop the genetic_variant_genome_builds table
    op.drop_table('genetic_variant_genome_builds')

