import click

from stactools.gap.utils import tile_to_mgrs_grid


def create_gap_command(cli):
    """Creates the USGS GAP command line utility."""
    @cli.group("gap", short_help="Work with USGS GAP data")
    def gap():
        pass

    @gap.command("tile", help="Tiles the input COG to an MGRS grid")
    @click.argument("infile")
    @click.argument("outdir")
    def tile_command(infile, outdir):
        """Tiles the input file to the MGRS grid.

        The source GAP data are huge GeoTIFFS, so we tile the geotiffs to the MGRS grid.
        """
        tile_to_mgrs_grid(infile, outdir)
