RPI_SGP30
=========

Program to read eCO_2 and TVOC from the `SGP30 sensor <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Sensirion_Gas_Sensors_SGP30_Datasheet_EN.pdf>`_. Based on the smbus2 i2c library for ease of use.


Quick usage-example:
--------------------
::

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

Features that are known to be missing (listing in rough order of importance):
-----------------------------------------------------------------------------
* Fix python3 compatibility.
* The handing of baseline values are not that great, it should probably be up to the end user to save and restore them as needed.
* Write doc-strings for all or at least most methods.
* reading raw-values.
* A more "driver like" class that took care of all chip identification, polling intervals store baseline and so on.

Hardware notices:
-----------------
If you have the AdaFruit board with built in level shifters and voltage regulator it is should work if you just plug in `SDA to pin 3, SCL to pin 5, VCC to pin 17 and GND to pin 20 <https://pinout.xyz/pinout/i2c>`_. You should then be able to find the SGP30 an address 0x58 using `i2cdetect -y 1`. If you get an error message  you probbably need to enable i2c in the kernel using  `raspi-config and reboot <https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial>`_

