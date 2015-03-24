import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap

class FujitsuLogicalDiskMap(SnmpPlugin):

    maptype = "LogicalDiskMap"
    modname = "ZenPacks.community.FujiMon.FujitsuLogicalDisk"
    relname = "logicaldisks"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('virtualDiskTable',
                    '1.3.6.1.4.1.231.2.49.1.6.2.1',
                    {
                        '.3': 'size',
                        '.5': 'diskType',
                        '.7': 'stripesize',
                        '.11': 'id',
                        '.12': '_sizeM',
                        '.14': 'description',
                        '.19': 'status',
                    }
        ),
    )

    diskTypes = {1: 'UNKNOWN',
                2: 'RAID0',
                3: 'RAID01',
                4: 'RAID1',
                5: 'RAID1e',
                6: 'RAID10',
                7: 'RAID3',
                8: 'RAID4',
                9: 'RAID5',
                10: 'RAID50',
                11: 'RAID5e',
                12: 'RAID5ee',
                13: 'RAID6',
                14: 'CONCATl',
                15: 'SINGLE',
                16: 'RAID60',
                17: 'RAID1e0',
                18: 'RAID0CC',
                19: 'RAID1CC',
                20: 'RAID1ECC',
                21: 'RAID5CC',
                22: 'RAID00',
                }

    def process(self, device, results, log):
        
	log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, disk in tabledata.get('virtualDiskTable', {}).iteritems():
            try:
                om = self.objectMap(disk)
                om.id = self.prepId(om.id)
                om.snmpindex = oid.strip('.')
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1),
                                                    'Unknown (%d)'%om.diskType)
                om.stripesize = int(getattr(om, '_stripesizeM', 0)
                                ) * 1048576 + int(getattr(om, 'stripesize', 0))
                om.size = int(getattr(om, '_sizeM', 0)
                                ) * 1048576 + int(getattr(om, 'size', 0))
            except AttributeError:
                continue
            rm.append(om)
        return rm
