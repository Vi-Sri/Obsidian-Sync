import unittest

import obsidian-sync


class VersionTestCase(unittest.TestCase):
    """ Version tests """

    def test_version(self):
        """ check obsidian-sync exposes a version attribute """
        self.assertTrue(hasattr(obsidian-sync, "__version__"))
        self.assertIsInstance(obsidian-sync.__version__, str)


if __name__ == "__main__":
    unittest.main()
