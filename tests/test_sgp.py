from .context import sgp30

from mock_smbus2 import MockSMBus
import unittest
class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    def setUp(self):
        self.bus = MockSMBus()
    def test_init(self):
        b=sgp30.sgp30.Sgp30(self.bus)
        b.init_sgp()
