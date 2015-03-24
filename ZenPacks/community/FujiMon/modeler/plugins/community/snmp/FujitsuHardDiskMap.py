from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class FujitsuHardDiskMap(SnmpPlugin):

    maptype = "HardDiskMap"
    modname = "ZenPacks.community.FujiMon.FujitsuHardDisk"
    relname = "harddisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('arrayDiskTable',
                    '1.3.6.1.4.1.231.2.49.1.5.2.1',
                    {
                        '.2': 'snmpindex',
			'.3': 'tag',
                        '.24': 'description',
                        '.6': '_manuf',
                        '.20': 'status',
                        '.5': '_model',
                        '.17': 'serialNumber',
                        '.16': 'FWRev',
                        '.21': '_sizeM',
                        '.7': 'size',
                        '.23': 'bay',
                        '.11': 'diskType',
                        #'.8': 'rpm',
                    }
        ),
        GetTableMap('arrayLocationTable',
                    '1.3.6.1.4.1.231.2.49.1.5.2.1',
                    {
                        '.2': 'snmpindex',
                        '.1': 'chassis',
                    }
        ),
    )

    diskTypes = {1: 'OTHER',
                2: 'SCSI',
                3: 'IDE',
                4: 'IEEE1394',
                5: 'SATA',
                6: 'SAS',
                7: 'FC',
                8: '',
                }

    def process(self, device, results, log):
        
	log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        diskLocation = tabledata.get('arrayLocationTable')
        rm = self.relMap()
        for oid, disk in tabledata.get('arrayDiskTable', {}).iteritems():
            try:
                om = self.objectMap(disk)
		om.snmpindex = oid.strip('.')
		om.rpm = 0
                chassis = tabledata.get('arrayLocationTable', {}).get(oid,
                                                {}).get('chassis', 'Backplane')
                om.id = self.prepId("%s %s" % (chassis, om.description))
                om._model = getattr(om, '_model', '') or 'hard disk'
                om._manuf = getattr(om, '_manuf', '') or 'Unknown'
                om.description = "%s %s" % (om._manuf, om._model)
                om.setProductKey = MultiArgs(om._model, om._manuf)
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1),
                                                    'Unknown (%d)'%om.diskType)
                om.size = int(getattr(om, '_sizeM', 0)) * 1048576 + int(
                                                        getattr(om, 'size', 0))
            except AttributeError:
                continue
            rm.append(om)
        return rm
