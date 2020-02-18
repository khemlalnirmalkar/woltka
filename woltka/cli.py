#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# Copyright (c) 2020--, Qiyun Zhu.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click

from .classify import classify as _classify


@click.version_option('0.1.0')
@click.group()
def cli():
    pass


# `gotu` is a simplified wrapper of `classify`

@cli.command('gotu')
@click.option(
    '--input', '-i', 'input_fp', required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='input read alignment directory')
@click.option(
    '--output', '-o', 'output_fp', required=True,
    type=click.Path(writable=True),
    help=('output gOTU table)'))
@click.option(
    '--multi/--no-multi', default=True,
    help=('allow one sequence to be assigned to multiple gOTUs; each hit '
          'will be counted as 1 / k (k is the totally number of hits)'))
@click.option(
    '--ixend/--no-ixend', default=False,
    help=('subject identifiers end with underscore index, the latter of which '
          'is to be removed prior to mapping.'))
@click.pass_context
def gotu(ctx, **kwargs):
    """Generate a gOTU table based on sequence alignments.
    """
    ctx.invoke(classify, **kwargs)


# `classify` invokes the main classification workflow

@cli.command('classify')
# input and output
@click.option(
    '--input', '-i', 'input_fp', required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='directory of input read alignment(s)')
@click.option(
    '--output', '-o', 'output_fp', required=True,
    type=click.Path(writable=True),
    help=('path to output profile file (single rank) or directory (multiple '
          'ranks)'))
# input information
@click.option(
    '--format', '-f', 'input_fmt', default='auto',
    type=click.Choice(['auto', 'b6o', 'sam', 'map'], case_sensitive=False),
    help=('format of read alignment: "auto": automatic determination '
          '(default), "b6o": BLAST tabular format (-outfmt 6), "sam": SAM '
          'format, "map": simple map of query <tab> subject'))
@click.option(
    '--extension', '-e', 'input_ext',
    help='input filename extension following sample ID')
@click.option(
    '--sample-ids', '-s', type=click.File('r'),
    help='list of sample IDs to be included')
# behavior
@click.option(
    '--rank', '-r', 'rank_lst', type=click.STRING,
    help=('classify sequences at this rank; ignore or enter "none" to omit '
          'classification; enter "free" for free-rank classification; can '
          'specify multiple comma-delimited ranks and one profile will be '
          'generated for each rank'))
@click.option(
    '--multi/--no-multi', default=True,
    help=('allow one sequence to be assigned to multiple classification '
          'units at the same rank; per-unit match counts will be recorded '
          'and profile will be normalized by total number of matches'))
@click.option(
    '--lca/--no-lca', default=True,
    help=('attempt to find lowest common ancestor (LCA) in taxonomy for '
          'non-unique matches; note: root is not assumed unless defined, '
          'and there may be multiple LCAs, in which case each is counted '
          'once; results are then subject to ambiguity treatment'))
@click.option(
    '--ixend/--no-ixend', default=False,
    help=('subject identifiers end with underscore index, the latter of which '
          'is to be removed prior to mapping.'))
# gene information
@click.option(
    '--coords', '-c', 'coords_fp', type=click.Path(exists=True),
    help=('table of coordinates of genes on reference genomes, with which '
          'sequence-to-genome alignment will be translated into sequence-to-'
          'gene mapping'))
# tree information
@click.option(
    '--map', '-m', 'map_fps', type=click.Path(exists=True), multiple=True,
    help=('map(s) of subjects to higher classification units, such as '
          'nucleotides to host genomes, sequence IDs to taxonomy IDs, gene '
          'family to pathway, etc., can accept multiple maps entered in low-'
          'to-high order'))
@click.option(
    '--names', 'names_fp', type=click.Path(exists=True),
    help=('map of taxonomic units to labels; can be plain map or NCBI '
          'names.dmp'))
@click.option(
    '--nodes', 'nodes_fp', type=click.Path(exists=True),
    help=('hierarchical structure of taxonomy defined by NCBI names.dmp '
          'or compatible format'))
@click.option(
    '--newick', 'newick_fp', type=click.Path(exists=True),
    help=('classification hierarchies defined by a tree in Newick format.'))
@click.option(
    '--rank-table', 'ranktb_fp', type=click.Path(exists=True),
    help=('classification hierarchies defined by a table with each column '
          'representing a level and header as level name.'))
@click.option(
    '--lineage', 'lineage_fp', type=click.Path(exists=True),
    help=('map of subjects/groups to lineage strings in format of "taxonomic;'
          'units;from;high;to;low", can be Greengenes-style taxonomy where '
          'level codes such as "k__" will be parsed'))
def classify(**kwargs):
    """Generate a profile of samples based on a classification system.
    """
    _classify(**kwargs)


if __name__ == '__main__':
    cli()
