import datetime
import unittest

from pystac.extensions.projection import ProjectionExtension
from pyproj import CRS

from stactools.gap.stac import create_item
from tests import test_data


class StacTest(unittest.TestCase):
    def test_create_item(self):
        infile = test_data.get_path(
            "data-files/GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011.XML")
        item = create_item(infile)
        self.assertEqual(item.id,
                         "GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011")
        self.assertIsNotNone(item.geometry)
        self.assertEqual(item.bbox,
                         [-128.446443, 22.0670194, -64.761475, 52.496415])
        self.assertEqual(item.links, [])  # TODO add links
        self.assertEqual(item.assets, {})  # TODO add assets
        self.assertIsNone(item.collection_id)
        self.assertEqual(item.datetime,
                         datetime.datetime(2016, 5, 13, 0, 0, 0))
        self.assertFalse(ProjectionExtension.has_extension(item))
        item.validate()

    def test_create_item_with_tif(self):
        infile = test_data.get_path(
            "data-files/GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011.XML")
        tif = test_data.get_path(
            "data-files/gap_landfire_nationalterrestrialecosystems2011_subset.tif"
        )
        item = create_item(infile, tif)
        self.assertEqual(
            item.id, "gap_landfire_nationalterrestrialecosystems2011_subset")
        self.assertIsNotNone(item.geometry)
        self.assertEqual(item.bbox, [
            -110.00025443243528, 29.359168172694346, -99.94710283198935,
            40.69658382856684
        ])
        self.assertTrue(ProjectionExtension.has_extension(item))
        projection = ProjectionExtension.ext(item)
        self.assertIsNone(projection.epsg)
        with open(test_data.get_path("data-files/srs.wkt2")) as f:
            source_srs = CRS.from_wkt(f.read())
        self.assertEqual(CRS.from_wkt(projection.wkt2), source_srs)
        self.assertEqual(projection.shape, [120, 80])
        self.assertEqual(projection.transform, [
            10000.0, 0.0, -1180455.0, 0.0, -10000.0, 1974105.0, 0.0, 0.0, 1.0
        ])
        item.validate()
