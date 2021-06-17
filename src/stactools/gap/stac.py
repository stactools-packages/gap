import os.path
from typing import Optional

from pystac import Item

from stactools.gap import Metadata


def create_item(xml_href: str, tif_href: Optional[str] = None) -> Item:
    """Creates a STAC Item from an href to the metadata.

    Optionally allows a tile .tif to be provided, in which case the tile will be
    used to set the bounds instead of the XML metadata.
    """
    metadata = Metadata.from_href(xml_href)
    id = os.path.splitext(os.path.basename(xml_href))[0]
    if tif_href:
        return metadata.create_item(tif_href=tif_href)
    else:
        return metadata.create_item(id=id)
