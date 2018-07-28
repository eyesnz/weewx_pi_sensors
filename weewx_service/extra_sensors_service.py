import syslog
import weewx
from weewx.wxengine import StdService
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT as dht


class ExtraSensorsService(StdService):
    def __init__(self, engine, config_dict):
        super(ExtraSensorsService, self).__init__(engine, config_dict)      
        d = config_dict.get('ExtraSensorsService', {})
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.load_data)
    
    def load_data(self, event):
        try:
            self.get_bmp180(event)
            self.get_dht22(event)
        except Exception, e:
            syslog.syslog(syslog.LOG_ERR, "extrasensors: cannot read value: %s" % e) 

    # Get BMP180 data
    def get_bmp180(self, event):
        sensor = BMP085.BMP085()
        mbarToinHg = 0.02952998751

        pressure = float(sensor.read_pressure()/100.0)
        syslog.syslog(syslog.LOG_DEBUG, "extrasensors: found pressure value of %s mbar" % pressure)
        event.record['pressure'] = float(pressure * mbarToinHg)

    # Get DHT22 data
    def get_dht22(self, event):
        humidity, temperature = dht.read_retry(dht.DHT22, 22) #Use pin 22
        if humidity is not None:
            syslog.syslog(syslog.LOG_DEBUG, "extrasensors: found humidity value of %s" % humidity)
            event.record['inHumidity'] = float(humidity)
        if temperature is not None:
            syslog.syslog(syslog.LOG_DEBUG, "extrasensors: found temperature value of %s C" % temperature)
            event.record['inTemp'] = float(temperature * 9.0/5.0 + 32)
