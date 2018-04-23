RPI_SGP30
=========

Library to read |eCO_2| and TVOC from the `SGP30 sensor <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Sensirion_Gas_Sensors_SGP30_Datasheet_EN.pdf>`_. Based on the smbus2 i2c library for ease of use.

It should be compatible with both python 2 and 3 but is currently only tested under Python 2.7

Quick usage-example:
--------------------
::

    from smbus2 import SMBusWrapper
    from sgp30 import Sgp30
    import time
    with SMBusWrapper(1) as bus:
        sgp=Sgp30(bus,baseline_filename="/tmp/mySGP30_baseline") #things thing with the baselinefile is dumb and will be changed in the future
        print("resetting all i2c devices")
        sgp.i2c_geral_call() #WARNING: Will reset any device on teh i2cbus that listens for general call
        print(sgp.read_features())
        print(sgp.read_serial())
        sgp.init_sgp()
        print(sgp.read_measurements())
        print("the SGP30 takes at least 15 seconds to warm up, 12 hours before the readigs become really stable"
     	  for i in range(20):
     		  time.sleep(1)
     		  print(".",end="")
     	  print()
           print(sgp.read_measurements())

Current design considerations:
------------------------------
The class strives to to be light-weight and portable. It is currently a bit to tightly bound to the smbus2 class. In most cases I try to ease of readability rather than purity or speed.

Features that are known to be missing (listing in rough order of importance):
-----------------------------------------------------------------------------
* The handing of baseline values is not that great, it should probably be up to the end user to save and restore them as needed.
* Write doc-strings for all or at least most methods.
* reading raw-values.
* A more "driver like" class that takes care of all chip identification, polling at regular intervals, restoring baseline and so on.
* Run real hardware tests under Python3

Hardware notices:
-----------------
If you have the Adafruit board with built in level shifters and voltage regulator it is should work if you just plug in `SDA to pin 3, SCL to pin 5, VCC to pin 17 and GND to pin 20 <https://pinout.xyz/pinout/i2c>`_. You should then be able to find the SGP30 an address 0x58 using `i2cdetect -y 1`. If you get an error message  you probably need to enable i2c in the kernel using  `raspi-config and reboot <https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial>`_


Feel free to contact me with bugs, questions or issues.

.. |eCO_2| replace:: eCO\ :sub:`2`
