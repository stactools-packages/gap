import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from shapely.geometry import box, mapping

from stactools.core.io import read_text


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

    def __init__(self, xml: Element) -> None:
        west = float(xml.findtext("./idinfo/spdom/bounding/westbc"))
        east = float(xml.findtext("./idinfo/spdom/bounding/eastbc"))
        south = float(xml.findtext("./idinfo/spdom/bounding/southbc"))
        north = float(xml.findtext("./idinfo/spdom/bounding/northbc"))
        self.bbox = [west, south, east, north]
        self.geometry = mapping(box(*self.bbox))
        self.datetime = datetime.datetime.strptime(
            xml.findtext("./idinfo/citation/citeinfo/pubdate"), r"%Y%m%d")
