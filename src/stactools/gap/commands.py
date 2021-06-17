import os

import click

from pystac import Collection, Extent

from stactools.gap.constants import DEFAULT_TILE_SIZE
from stactools.gap.stac import create_item
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

        The source GAP data are huge GeoTIFFS, so we tile the geotiffs.
        """
        tile(infile, outdir, size)

    @gap.command("create-collection",
                 help="Creates a tiled collection from a single huge GAP TIFF")
    @click.argument("infile")
    @click.argument("cog_directory")
    @click.argument("stac_directory")
    @click.option("-s", "--tile-size", default=DEFAULT_TILE_SIZE)
    def create_collection_command(infile, cog_directory, stac_directory,
                                  tile_size):
        """Creates a tiled collection from a single huge GAP TIFF.

        Will create the COG and STAC directories if needed.
        """
        id = os.path.splitext(os.path.basename(infile))[0]
        os.makedirs(cog_directory, exist_ok=True)
        tile(infile, cog_directory, tile_size)
        items = []
        for path in (os.path.join(cog_directory, file_name)
                     for file_name in os.listdir(cog_directory)):
            item = create_item(path)
            items.append(item)
        extent = Extent.from_items(items)
        collection = Collection(id=id,
                                description="",
                                extent=extent,
                                title="",
                                datetime=None)
        collection.set_self_href(
            os.path.join(stac_directory, "collection.json"))
        collection.validate_all()
        collection.save()
