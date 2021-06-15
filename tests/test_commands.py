import os.path
from tempfile import TemporaryDirectory

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
            result = self.run_command(["gap", "tile", infile, directory])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))
            for file in os.listdir(directory):
                print(file)
        self.assertTrue(False)
