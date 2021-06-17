import os.path

from pystac import Item

from stactools.gap import Metadata


def create_item(href: str) -> Item:
    """Creates a STAC Item from an href to the metadata.

    Optionally allows a tile .tif to be provided, in which case the tile will be
    used to set the bounds instead of the XML metadata.
    """
    metadata = Metadata.from_href(href)
    item = Item(id=os.path.splitext(os.path.basename(href))[0],
                geometry=metadata.geometry,
                bbox=metadata.bbox,
                properties={},
                datetime=metadata.datetime)
    return item
