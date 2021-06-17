import os.path
from typing import Optional

from pystac import Item
from pystac.extensions.projection import ProjectionExtension
import rasterio
from shapely.geometry import mapping, box, shape

from stactools.core.projection import reproject_geom

from stactools.gap import Metadata


def create_item(xml_href: str, tif_href: Optional[str] = None) -> Item:
    """Creates a STAC Item from an href to the metadata.

    Optionally allows a tile .tif to be provided, in which case the tile will be
    used to set the bounds instead of the XML metadata.
    """
    metadata = Metadata.from_href(xml_href)
    projection_properties = {}
    if tif_href:
        id = os.path.splitext(os.path.basename(tif_href))[0]
        with rasterio.open(tif_href) as dataset:
            source_crs = dataset.crs
            source_bbox = dataset.bounds
            source_geometry = mapping(box(*source_bbox))
            source_shape = [dataset.height, dataset.width]
            source_transform = list(dataset.transform)
        geometry = reproject_geom(source_crs, "EPSG:4326", source_geometry)
        bbox = list(shape(geometry).bounds)
        projection_properties = {
            "epsg": None,
            "wkt2": source_crs.to_wkt(),
            "shape": source_shape,
            "transform": source_transform,
        }
    else:
        id = os.path.splitext(os.path.basename(xml_href))[0]
        geometry = metadata.geometry
        bbox = metadata.bbox
    item = Item(id=id,
                geometry=geometry,
                bbox=bbox,
                properties={},
                datetime=metadata.datetime)

    if projection_properties:
        ProjectionExtension.add_to(item)
        projection = ProjectionExtension.ext(item)
        projection.apply(**projection_properties)

    return item
