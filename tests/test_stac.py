import datetime

from pystac import MediaType
from pystac.extensions.projection import ProjectionExtension
from pyproj import CRS

from stactools.gap.stac import create_item
from tests import test_data
from tests.utils import StactoolsTestCase


class StacTest(StactoolsTestCase):
    def test_create_item(self):
        infile = test_data.get_path(
            "data-files/GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011.xml")
        item = create_item(infile)
        self.assertEqual(item.id,
                         "GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011")
        self.assertIsNotNone(item.geometry)
        self.assertEqual(item.bbox,
                         [-128.446443, 22.0670194, -64.761475, 52.496415])
        self.assertEqual(item.links, [])  # TODO add links
        self.assertEqual(item.assets, {})  # TODO add assets
        self.assertIsNone(item.collection_id)
        self.assertEqual(
            item.datetime,
            datetime.datetime(2011,
                              12,
                              31,
                              0,
                              0,
                              0,
                              tzinfo=datetime.timezone.utc))
        self.assertEqual(
            item.common_metadata.start_datetime,
            datetime.datetime(2010,
                              1,
                              1,
                              0,
                              0,
                              0,
                              tzinfo=datetime.timezone.utc))
        self.assertEqual(
            item.common_metadata.end_datetime,
            datetime.datetime(2011,
                              12,
                              31,
                              0,
                              0,
                              0,
                              tzinfo=datetime.timezone.utc))
        self.assertFalse(ProjectionExtension.has_extension(item))
        item.validate()

    def test_create_item_with_tif(self):
        infile = test_data.get_path(
            "data-files/GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011.xml")
        tif_path = test_data.get_path(
            "data-files/gap_landfire_nationalterrestrialecosystems2011_subset.tif"
        )
        item = create_item(infile, tif_path)
        self.assertEqual(
            item.id, "gap_landfire_nationalterrestrialecosystems2011_subset")
        self.assertIsNotNone(item.geometry)
        expected_bbox = [
            -110.00025443243528, 29.359168172694346, -99.94710283198935,
            40.69658382856684
        ]
        self.assertListsAreClose(item.bbox, expected_bbox, 1e-4)
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

        tif = item.assets["data"]
        self.assertEqual(tif.href, tif_path)
        self.assertEqual(tif.title, "GeoTIFF data")
        self.assertEqual(tif.media_type, MediaType.COG)
        self.assertEqual(tif.roles, ["data"])

        item.validate()
