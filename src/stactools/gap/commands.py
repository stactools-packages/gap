import click

from stactools.gap.constants import DEFAULT_TILE_SIZE
from stactools.gap.utils import tile


def create_gap_command(cli):
    """Creates the USGS GAP command line utility."""
    @cli.group("gap", short_help="Work with USGS GAP data")
    def gap():
        pass

    @gap.command("tile", help="Tiles the input COG to a grid")
    @click.argument("infile")
    @click.argument("outdir")
    @click.option("-s", "--size", default=DEFAULT_TILE_SIZE)
    def tile_command(infile, outdir, size):
        """Tiles the input file to the MGRS grid.

        The source GAP data are huge GeoTIFFS, so we tile the geotiffs to the MGRS grid.
        """
        tile(infile, outdir, size)
