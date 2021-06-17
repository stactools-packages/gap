import datetime
import unittest

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
        # TODO check proj extension
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
        item.validate()
