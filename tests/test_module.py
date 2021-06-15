import unittest

import stactools.gap


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.gap.__version__)
