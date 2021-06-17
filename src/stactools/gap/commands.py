import os
import sys

import click

from pystac import Collection, Extent

from stactools.gap import Metadata
from stactools.gap.constants import DEFAULT_TILE_SIZE, KEYWORDS, PROVIDERS
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
    @click.argument("xml_href")
    @click.argument("tif_href")
    @click.argument("cog_directory")
    @click.argument("stac_directory")
    @click.option("-s", "--tile-size", default=DEFAULT_TILE_SIZE)
    def create_collection_command(xml_href, tif_href, cog_directory,
                                  stac_directory, tile_size):
        """Creates a tiled collection from a single huge GAP TIFF.

        Will create the COG and STAC directories if needed.
        """
        if os.path.splitext(xml_href)[1] != ".xml":
            print(
                f"{xml_href} does not look like an xml file, make sure it has an 'xml' extension",
                file=sys.stderr)
            sys.exit(1)
        metadata = Metadata.from_href(xml_href)
        os.makedirs(cog_directory, exist_ok=True)
        tile(tif_href, cog_directory, tile_size)
        items = []
        for tif_path in (os.path.join(cog_directory, file_name)
                         for file_name in os.listdir(cog_directory)):
            item = metadata.create_item(tif_path)
            items.append(item)
        extent = Extent.from_items(items)
        collection = Collection(id=os.path.splitext(
            os.path.basename(xml_href))[0],
                                description=metadata.description,
                                extent=extent,
                                title=metadata.title)
        collection.keywords = KEYWORDS
        collection.providers = PROVIDERS
        collection.set_self_href(
            os.path.join(stac_directory, "collection.json"))
        collection.validate_all()
        collection.save()
