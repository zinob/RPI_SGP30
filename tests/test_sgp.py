from .context import sgp30

from mock_smbus2 import MockSMBus
import unittest

class TestConstructor(unittest.TestCase):
    """Basic test cases."""
    def setUp(self):
        self.bus = MockSMBus()
    def test_init(self):
        b=sgp30.sgp30.Sgp30(self.bus)
        b.init_sgp()

class SimpleTest(unittest.TestCase):
    """Basic test cases."""
    def setUp(self):
        self.bus = MockSMBus()
        self.sgp=sgp30.sgp30.Sgp30(self.bus)
    def test_read(self):
        self.sgp.read_measurements()
