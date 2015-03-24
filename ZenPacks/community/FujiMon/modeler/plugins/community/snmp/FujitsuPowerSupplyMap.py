from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class PowerSupplyMap(SnmpPlugin):

    maptype = "PowerSupplyMap"
    modname = "ZenPacks.community.FujiMon.FujitsuPowerSupply"
    relname = "powersupplies"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('powerSupplyTable',
                    '.1.3.6.1.4.1.231.2.10.2.2.10.6.2.1',
                    {
                        '.3': '_location',
                        '.5': 'status',
                        '.7': 'watts',
                    }
        )
    )

    typemap =  {1: 'Other',
                2: 'Unknown',
                3: 'Linear',
                4: 'Switching',
                5: 'Battery',
                6: 'UPS',
                7: 'Converter',
                8: 'Regulator',
                9: 'AC',
                10: 'DC',
                11: 'VRM',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, ps in tabledata.get('powerSupplyTable', {}).iteritems():
            try:
                om = self.objectMap(ps)
                if getattr(om, 'status', 0) != 2: continue
                om.snmpindex = oid.strip('.')
                om.id = self.prepId(getattr(om, '_location', 'Unknown'))
                om.type = self.typemap.get(getattr(om,'type',1),
                                                        'Other (%d)'%om.type)
            except AttributeError:
                continue
            rm.append(om)
        return rm
