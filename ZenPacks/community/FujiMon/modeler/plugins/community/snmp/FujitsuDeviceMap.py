from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs


class FujitsuDeviceMap(SnmpPlugin):

    maptype = "FujitsuDeviceMap" 

    snmpGetMap = GetMap({ 
        '.1.3.6.1.4.1.231.2.10.2.1.4.0': 'setOSProductKey',
        '.1.3.6.1.4.1.231.2.10.2.2.5.10.3.1.4.0' : 'setHWProductKey',
        '.1.3.6.1.4.1.231.2.10.2.2.5.10.3.1.3.0' : 'setHWSerialNumber',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata.get('setHWProductKey') is None: return None
        om = self.objectMap(getdata)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, "Fujitsu")
        return om

