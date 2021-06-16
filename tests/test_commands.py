import os.path
from tempfile import TemporaryDirectory

import rasterio

from stactools.gap.commands import create_gap_command
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
