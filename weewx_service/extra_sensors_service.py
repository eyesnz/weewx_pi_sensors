import syslog
import weewx
from weewx.wxengine import StdService
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT as dht


class ExtraSensorsService(StdService):
    def __init__(self, engine, config_dict):
        super(ExtraSensorsService, self).__init__(engine, config_dict)      
        d = config_dict.get('ExtraSensorsService', {})
        # Read from config which pin to use on the RPI GPIO
        # Defaults to 22
        self.dht22_pin = d.get('dht22_pin', 22)
        # Use the loop packet event as that allows data to still get into the WeeWX database
        # as well as supporting a OLED module on the RPI
        self.bind(weewx.NEW_LOOP_PACKET, self.load_data)
    
    def load_data(self, event):
        try:
            self.get_bmp180(event)
            self.get_dht22(event)
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, "extrasensors: cannot read value: %s" % e) 

    # Get BMP180 data
    def get_bmp180(self, event):
        sensor = BMP085.BMP085()

        pressure = float(sensor.read_pressure()/100.0)
        syslog.syslog(syslog.LOG_DEBUG, "extrasensors: found pressure value of %s mbar" % pressure)
        # NOTE: stores as mbar
        event.packet['pressure'] = float(pressure)

    # Get DHT22 data
    def get_dht22(self, event):
        humidity, temperature = dht.read_retry(dht.DHT22, self.dht22_pin)
        if humidity is not None:
            syslog.syslog(syslog.LOG_DEBUG, "extrasensors: found humidity value of %s %%" % humidity)
            event.packet['inHumidity'] = float(humidity)
        if temperature is not None:
            syslog.syslog(syslog.LOG_DEBUG, "extrasensors: found temperature value of %s C" % temperature)
            # NOTE: stores as celsius
            event.packet['inTemp'] = float(temperature)
