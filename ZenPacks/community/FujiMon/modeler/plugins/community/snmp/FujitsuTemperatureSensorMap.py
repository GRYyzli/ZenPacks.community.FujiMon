from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class FujitsuTemperatureSensorMap(SnmpPlugin):

    maptype = "TemperatureSensorMap"
    modname = "ZenPacks.community.FujiMon.FujitsuTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('temperatureProbeTable',
                    '.1.3.6.1.4.1.231.2.10.2.2.10.5.1.1',
                    {
                        '.5': 'status',
                        #'.7': '_type',
                        '.3': 'id',
                        '.7': 'threshold',
                    }
        ),
    )

    def process(self, device, results, log):
        
	log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        tsensorstable = tabledata.get("temperatureProbeTable")
        rm = self.relMap()
        for oid,tsensor in tabledata.get("temperatureProbeTable",{}).iteritems():
            try:
                om = self.objectMap(tsensor)
                if om.status == 2: continue
                om.id = self.prepId(getattr(om, 'id', 'Unknown'))
                om.snmpindex = oid.strip('.')
                #if om._type == 16:
                #    om.modname = "ZenPacks.community.FujiMon.FujitsuDiscreteTemperatureSensor"
                #    om.threshold = 1
            except AttributeError:
                continue
            rm.append(om)
        return rm
