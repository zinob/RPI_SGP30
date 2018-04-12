from .context import sgp30

import unittest
class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    def test_absolute_truth_and_meaning(self):
        self.assertEqual(sgp30.Crc8().hash([0xBE, 0xEF]), 0x92,"testing doccumentation example")
        self.assertEqual(sgp30.Crc8().hash([1,144]), 76, "First half of default reading")
        self.assertEqual(sgp30.Crc8().hash([0,6]), 39, "second half of default reading, ")

