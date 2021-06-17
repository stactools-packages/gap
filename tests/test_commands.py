import datetime
import os.path
from tempfile import TemporaryDirectory

import pystac
from pystac import SpatialExtent, TemporalExtent
import rasterio

from stactools.gap.commands import create_gap_command
from stactools.gap.constants import PROVIDERS
from stactools.testing import CliTestCase
from tests import test_data


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_gap_command]

    def test_tile(self):
        infile = test_data.get_path(
            "data-files/gap_landfire_nationalterrestrialecosystems2011_subset.tif"
        )
        with TemporaryDirectory() as directory:
            result = self.run_command(
                ["gap", "tile", "--size", "500001", infile, directory])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))
            for path in (os.path.join(directory, file)
                         for file in os.listdir(directory)):
                with rasterio.open(path) as dataset:
                    data = dataset.read(1)
                    rows, cols = data.shape
                    self.assertLessEqual(rows, 500001)
                    self.assertLessEqual(cols, 500001)

    def test_collection(self):
        tif = test_data.get_path(
            "data-files/gap_landfire_nationalterrestrialecosystems2011_subset.tif"
        )
        xml = test_data.get_path(
            "data-files/GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011.xml")
        with TemporaryDirectory() as directory:
            cog_directory = os.path.join(directory, "cogs")
            stac_directory = os.path.join(directory, "stac")
            result = self.run_command([
                "gap", "create-collection", "--tile-size", "500001", xml, tif,
                cog_directory, stac_directory
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))
            collection_path = os.path.join(stac_directory, "collection.json")
            collection = pystac.read_file(collection_path)
            self.assertEqual(
                collection.id,
                "GAP_LANDFIRE_National_Terrestrial_Ecosystems_2011")
            self.assertEqual(
                collection.title,
                "GAP/LANDFIRE_National_Terrestrial_Ecosystems_2011")
            self.assertEqual(
                collection.description,
                "The GAP National Terrestrial Ecosystems - Ver 3.0 is a 2011 update of the National Gap Analysis Program Land Cover Data - Version 2.2 for the conterminous U.S. The GAP National Terrestrial Ecosystems - Version 3.0 represents a highly thematically detailed land cover map of the U.S. The map legend includes types described by NatureServe's Ecological Systems Classification (Comer et al. 2002) as well as land use classes described in the National Land Cover Dataset 2011 (Homer et al. 2015). These data cover the entire continental U.S. and are a continuous data layer. These raster data have a 30 m x 30 m cell resolution. GAP used the best information available to create the land cover data; however GAP seeks to improve and update these data as new information becomes available."  # noqa
            )
            self.assertEqual(
                collection.keywords,
                ["land cover", "vegetation", "ecology", "wildlife habitat"])
            self.assertEqual(collection.license, "proprietary")
            self.assertEqual(collection.providers, PROVIDERS)
            self.assertEqual(
                collection.extent.spatial.bboxes,
                SpatialExtent([-128.446443, 22.0670194, -64.761475,
                               52.496415]).bboxes)
            self.assertEqual(
                collection.extent.temporal.intervals,
                TemporalExtent([
                    datetime.datetime(2010,
                                      1,
                                      1,
                                      0,
                                      0,
                                      0,
                                      tzinfo=datetime.timezone.utc),
                    datetime.datetime(2011,
                                      12,
                                      31,
                                      0,
                                      0,
                                      0,
                                      tzinfo=datetime.timezone.utc)
                ]).intervals)
            self.assertTrue(collection.summaries.is_empty())
            self.assertEqual(collection.assets, {})
            collection.validate_all()
