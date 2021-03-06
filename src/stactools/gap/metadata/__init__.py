import datetime
import os.path
import pkg_resources
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from pystac import Item, Asset, MediaType
from pystac.extensions.projection import ProjectionExtension
import rasterio
from shapely.geometry import box, mapping, shape

from stactools.core.io import ReadHrefModifier, read_text
from stactools.core.projection import reproject_geom

from stactools.gap.utils import is_conus


class Metadata:
    """USGS XML metadata for the GAP program."""
    @classmethod
    def from_href(cls, href: str) -> "Metadata":
        """Reads metadata from a href to the XML file."""
        text = read_text(href)
        return cls.from_text(text)

    @classmethod
    def from_text(cls, text: str) -> "Metadata":
        """Reads metadata from an XML string."""
        xml = ElementTree.fromstring(text)
        return cls(xml)

    @classmethod
    def from_raster(cls,
                    path: str,
                    read_href_modifier: Optional[ReadHrefModifier] = None
                    ) -> "Metadata":
        if is_conus(path, read_href_modifier=read_href_modifier):
            return Metadata.from_resource(
                "GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011.xml")
        else:
            return Metadata.from_resource("natgaplandcov_v2_metadata.xml")

    @classmethod
    def from_resource(cls, resource: str) -> "Metadata":
        return Metadata.from_text(
            pkg_resources.resource_string(__name__, resource))

    def __init__(self, xml: Element) -> None:
        west = float(xml.findtext("./idinfo/spdom/bounding/westbc"))
        east = float(xml.findtext("./idinfo/spdom/bounding/eastbc"))
        south = float(xml.findtext("./idinfo/spdom/bounding/southbc"))
        north = float(xml.findtext("./idinfo/spdom/bounding/northbc"))
        self._bbox = [west, south, east, north]
        self._geometry = mapping(box(*self._bbox))
        self._start_datetime = datetime.datetime(int(
            xml.findtext("./idinfo/timeperd/timeinfo/rngdates/begdate")),
                                                 1,
                                                 1,
                                                 0,
                                                 0,
                                                 0,
                                                 tzinfo=datetime.timezone.utc)
        self._end_datetime = datetime.datetime(int(
            xml.findtext("./idinfo/timeperd/timeinfo/rngdates/enddate")),
                                               12,
                                               31,
                                               0,
                                               0,
                                               0,
                                               tzinfo=datetime.timezone.utc)
        self.description = xml.findtext("./idinfo/descript/abstract")
        self.title = xml.findtext("./idinfo/citation/citeinfo/title").strip()

    def create_item(
            self,
            id: Optional[str] = None,
            tif_href: Optional[str] = None,
            read_href_modifier: Optional[ReadHrefModifier] = None) -> Item:
        """Creates a PySTAC Item from these metadata.

        Optionally uses the provided tif for bounds and projection information.
        """
        projection_properties = {}
        if tif_href:
            if not id:
                id = os.path.splitext(os.path.basename(tif_href))[0]
            if read_href_modifier:
                href = read_href_modifier(tif_href)
            else:
                href = tif_href
            with rasterio.open(href) as dataset:
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
        elif id:
            geometry = self._geometry
            bbox = self._bbox
        else:
            raise Exception(
                "Either id or tif_href must be provided to create an item from the metadata."
            )

        item = Item(id=id,
                    geometry=geometry,
                    bbox=bbox,
                    properties={
                        "start_datetime": self._start_datetime.isoformat(),
                        "end_datetime": self._end_datetime.isoformat(),
                    },
                    datetime=self._end_datetime)
        item.stac_extensions.append(
            "https://stac-extensions.github.io/processing/v1.0.0/schema.json")
        item.properties["processing:software"] = {
            "stactools-gap": pkg_resources.require("stactools-gap")[0].version
        }

        if projection_properties:
            ProjectionExtension.add_to(item)
            projection = ProjectionExtension.ext(item)
            projection.apply(**projection_properties)

        if tif_href:
            item.add_asset(
                "data",
                Asset(href=tif_href,
                      title="GeoTIFF data",
                      media_type=MediaType.COG,
                      roles=["data"]))

        return item
