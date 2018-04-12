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

    def test_general_call(self):
        b=sgp30.sgp30.Sgp30(self.bus)
        b.i2c_geral_call()
        self.assertEqual(self.bus.addr,0)
        self.assertEqual(self.bus.last,0x06)

class SimpleReadTests(unittest.TestCase):
    """Basic test cases."""
    def setUp(self):
        self.bus = MockSMBus()
        self.sgp=sgp30.sgp30.Sgp30(self.bus)
    def test_read(self):
        self.assertEqual(self.sgp.read_measurements().data,[400,6])
