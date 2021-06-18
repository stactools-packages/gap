import os
import sys

import click

from pystac import Collection, Extent

from stactools.gap import Metadata
from stactools.gap.constants import DEFAULT_TILE_SIZE, KEYWORDS, PROVIDERS
from stactools.gap.utils import tile


def eprint(message: str):
    print(message, file=sys.stderr)


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
    @click.argument("tile_directory")
    @click.argument("stac_directory")
    @click.option("-s", "--tile-size", default=DEFAULT_TILE_SIZE)
    @click.option("-t", "--tile-source", default=None)
    def create_collection_command(xml_href, tile_directory, stac_directory,
                                  tile_size, tile_source):
        """Creates a tiled collection from a single huge GAP TIFF.

        Will create the COG and STAC directories if needed.
        """
        if os.path.splitext(xml_href)[1] != ".xml":
            eprint(
                f"{xml_href} does not look like an xml file, make sure it has an 'xml' extension"
            )
            sys.exit(1)

        if tile_source:
            if os.path.isdir(tile_directory):
                eprint(
                    f"Tile directory {tile_directory} already exists, not overwriting"
                )
                sys.exit(1)
            os.makedirs(tile_directory)
            print(
                f"Tiling {tile_source} into {tile_directory} with tile size {tile_size}"
            )
            tile(tile_source, tile_directory, tile_size)
        elif not os.path.isdir(tile_directory):
            eprint(f"Tile directory {tile_directory} does not exist")
            sys.exit(1)
        elif not os.listdir(tile_directory):
            eprint(f"Tile directory {tile_directory} is empty")
            sys.exit(1)

        metadata = Metadata.from_href(xml_href)
        items = []
        for tif_path in (os.path.join(tile_directory, file_name)
                         for file_name in os.listdir(tile_directory)
                         if os.path.splitext(file_name)[1] == ".tif"):
            item = metadata.create_item(tif_href=tif_path)
            items.append(item)
        extent = Extent.from_items(items)
        collection = Collection(id=os.path.splitext(
            os.path.basename(xml_href))[0],
                                description=metadata.description,
                                extent=extent,
                                title=metadata.title)
        collection.keywords = KEYWORDS
        collection.providers = PROVIDERS
        collection.add_items(items)
        collection.set_self_href(
            os.path.join(stac_directory, "collection.json"))
        collection.normalize_hrefs(stac_directory)
        collection.validate_all()
        collection.save()
