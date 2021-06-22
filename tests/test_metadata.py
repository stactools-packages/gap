from unittest import TestCase

from stactools.gap import Metadata
from tests import test_data


class MetadataTest(TestCase):
    def test_from_tif_conus(self):
        tif_path = test_data.get_path(
            "data-files/gap_landfire_nationalterrestrialecosystems2011_subset.tif"
        )
        metadata = Metadata.from_raster(tif_path)
        self.assertEqual(metadata.title,
                         "GAP/LANDFIRE_National_Terrestrial_Ecosystems_2011")

    def test_from_tif_oconus(self):
        tif_path = test_data.get_path(
            "data-files/prgap_landcover_downsampled.img")
        metadata = Metadata.from_raster(tif_path)
        self.assertEqual(
            metadata.title,
            "National Gap Analysis Program Land Cover Data- Version 2")
