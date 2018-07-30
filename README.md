This adds extra sensor data to weewx by using the data_services feature.

Currently requires both a DHT22 for temperature and humidity data, and a BMP180 for Barometer/Pressure/Altitude data.

This works really well if combined with the `weewx-sdr` project, as you will be able to extract data from outside weather sensors and use the DHT22/BMP180 to get data for inside readings. i.e. Just like a Fine Offset console, without needing a console.

### Requirements

1. Raspberry PI
1. Weewx installed and working
1. A DHT22 connected to GPIO, preferably pin 22 (If connected differently, this can be changed in weewx.conf)
1. A BMP180 connected to GPIO, usually the SDA/SCL pins
1. Adafruit_Python_DHT installed and working (see https://github.com/adafruit/Adafruit_Python_DHT)
1. Adafruit_Python_BMP installed and working (see https://github.com/adafruit/Adafruit_Python_BMP)

### Install Instructions

1.  Copy the file in weewx_service/extra_sensors_service.py to the weewx user directory. This location could be different depending on how weewx was installed:

```
sudo cp weewx_service/extra_sensors_service.py /usr/share/weewx/user/
```

2.  Add the service to weewx.conf (NOTE: if you have existing data_services, then add this new service after your existing settings):

```
[Engine]
    [[Services]]
        data_services = user.extra_sensors_service.ExtraSensorsService,
```

3.  Restart weewx
