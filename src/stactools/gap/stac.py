import os.path

import rasterio
from pystac import Item
from shapely.geometry import box, mapping, shape
from stactools.core.projection import reproject_geom

from stactools.gap.constants import DATETIME


def create_item(href: str) -> Item:
    """Creates a STAC Item from an href."""
    with rasterio.open(href) as dataset:
        source_crs = dataset.crs
        source_bbox = dataset.bounds
    source_geometry = mapping(box(*source_bbox))
    geometry = reproject_geom(source_crs, "EPSG:4326", source_geometry)
    bbox = list(shape(geometry).bounds)
    item = Item(id=os.path.splitext(os.path.basename(href))[0],
                geometry=geometry,
                bbox=bbox,
                datetime=DATETIME,
                properties={})
j    return item
