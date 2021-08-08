from sps30 import SPS30
import time
from scd30_i2c import SCD30
import atexit

sps = SPS30(1)
scd30 = SCD30()

### Initialize SPS30 ##

print("starting sps30 particulate sensor...")
if sps.read_article_code() == sps.ARTICLE_CODE_ERROR:
    raise Exception("ARTICLE CODE CRC ERROR!")
else:
    print("ARTICLE CODE: " + str(sps.read_article_code()))

if sps.read_device_serial() == sps.SERIAL_NUMBER_ERROR:
    raise Exception("SERIAL NUMBER CRC ERROR!")
else:
    print("DEVICE SERIAL: " + str(sps.read_device_serial()))

#seconds = 604800
#sps.set_auto_cleaning_interval(seconds) # default 604800, set 0 to disable auto-cleaning
#sps.device_reset() # device has to be powered-down or reset to check new auto-cleaning interval

if sps.read_auto_cleaning_interval() == sps.AUTO_CLN_INTERVAL_ERROR: # or returns the interval in seconds
    raise Exception("AUTO-CLEANING INTERVAL CRC ERROR!")
else:
    print("AUTO-CLEANING INTERVAL: " + str(sps.read_auto_cleaning_interval()))

sps.start_measurement()
print("started sps30 particulate sensor...")

### DONE - Initialize SPS30 ##


### Initialize SCD30 ##
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()
### DONE - Initialize SPS30 ##

time.sleep(1)

#### MAIN CONTROL LOOP ##

while True:
    scd_ready = scd30.get_data_ready()
    sps_ready = sps.read_data_ready_flag()

    if scd_ready or sps_ready:
        if scd_ready:
            m = scd30.read_measurement()
            if m is not None:
                print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
        if sps_ready and sps_ready != sps.DATA_READY_FLAG_ERROR:
            if sps.read_measured_values() == sps.MEASURED_VALUES_ERROR:
                print("sps data read error")
            else:
                print(f"PM2.5: {sps.dict_values['pm2p5']}µg/mg, NC2.5: {sps.dict_values['nc2p5']} 1/cm3")
               # print ("PM1.0 V$alue in µg/m3: " + str(sps.dict_values['pm1p0']))
               # print ("PM2.5 Value in µg/m3: " + str(sps.dict_values['pm2p5']))
               # print ("PM4.0 Value in µg/m3: " + str(sps.dict_values['pm4p0']))
               # print ("PM10.0 Value in µg/m3: " + str(sps.dict_values['pm10p0']))
               # print ("NC0.5 Value in 1/cm3: " + str(sps.dict_values['nc0p5']))    # NC: Number of Concentration 
               # print ("NC1.0 Value in 1/cm3: " + str(sps.dict_values['nc1p0']))
               # print ("NC2.5 Value in 1/cm3: " + str(sps.dict_values['nc2p5']))
               # print ("NC4.0 Value in 1/cm3: " + str(sps.dict_values['nc4p0']))
               # print ("NC10.0 Value in 1/cm3: " + str(sps.dict_values['nc10p0']))
               # print ("Typical Particle Size in µm: " + str(sps.dict_values['typical']))	
    else:
        time.sleep(0.2)

### DONE ##

def stop_measurement():
    #sps.start_fan_cleaning()
    sps.stop_meaurement()

atexit.register(stop_meaurement)
