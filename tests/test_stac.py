import unittest

from stactools.gap.stac import create_item
from tests import test_data


class StacTest(unittest.TestCase):
    def test_create_item(self):
        infile = test_data.get_path(
            "data-files/gap_landfire_nationalterrestrialecosystems2011_subset.tif"
        )
        item = create_item(infile)
        self.assertEqual(
            item.id, "gap_landfire_nationalterrestrialecosystems2011_subset")
        item.validate()
