from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class FujitsuFanMap(SnmpPlugin):

    maptype = "FanMap"
    modname = "ZenPacks.community.FujiMon.FujitsuFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('coolingDeviceTable',
                    '.1.3.6.1.4.1.231.2.10.2.2.10.5.2.1',
                    {
                        '.3': '_locale',
                        '.5': 'status',
                    }
        ),
    )


    typemap = { 1: 'Other', 
                2: 'Unknown',
                3: 'Fan',
                4: 'Blower',
                5: 'Chip Fan',
                6: 'Cabinet Fan',
                7: 'Power Supply Fan',
                8: 'Heat Pipe',
                9: 'Refrigeration',
                10: 'Active Cooling',
                11: 'Passive Cooling',
                }


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, fan in tabledata.get('coolingDeviceTable', {}).iteritems():
            try:
                om = self.objectMap(fan)
                om.snmpindex = oid.strip('.')
                om.type = self.typemap.get(getattr(om, 'type', 2), 'Unknown')
                om.id = self.prepId(getattr(om, '_locale', 'Unknown'))
            except AttributeError:
                continue
            rm.append(om)
        return rm
