from .context import sgp30

from .mock_smbus2 import MockSMBus
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
        d=self.sgp.read_measurements()
        self.assertEqual(d.raw,[1, 144, 76, 0, 6, 39])
        self.assertEqual(d.data,[400,6])

    #No real need to do this super-carefully
    #or i will just be testing my own test code
    #just make sure that CRC test are used, maybe..
    def test_crc_ok(self):
        d=self.sgp.read_measurements()
        self.assertEqual(d.crc_ok,True)

    def test_crc_fail(self):
        bus=MockSMBus(break_crc=True)
        sgp=sgp30.sgp30.Sgp30(bus)
        d=sgp.read_measurements()
        self.assertEqual(d.data,[400,6])
        self.assertEqual(d.crc_ok,False)

class TestBaselineMethods(unittest.TestCase):
    """Basic tests for the load/save baseline-methods"""
    def setUp(self):
        self.bus = MockSMBus()
        self.sgp=sgp30.sgp30.Sgp30(self.bus,baseline_filename="/tmp/sgp-crc-test")
        fbus=MockSMBus(break_crc=True)
        self.fsgp=sgp30.sgp30.Sgp30(fbus)


    def test_save(s):
        s.assertTrue(s.sgp.store_baseline())
        open(s.sgp._baseline_filename).read()

    def test_save_fail(s):
        open(s.sgp._baseline_filename,"w").write("")
        s.assertFalse(s.fsgp.store_baseline(),"ensure broken crc is detected")
        s.assertEquals(open(s.sgp._baseline_filename).read(),"","ensure that broken data is not written")

    def test_save_load(s):
        s.assertTrue(s.sgp.store_baseline())
        s.assertTrue(s.sgp.try_set_baseline())

    def test_load_fail_crc(s):
        open(s.sgp._baseline_filename,"w").write("[133, 152, 0, 138, 32, 0]")
        s.assertFalse(s.sgp.try_set_baseline())

    def test_load_fail_broken_json(s):
        open(s.sgp._baseline_filename,"w").write("[133, 152, 0.. nope")
        s.assertFalse(s.sgp.try_set_baseline())
