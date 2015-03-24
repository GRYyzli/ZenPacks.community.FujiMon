from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class FujitsuCPUMap(SnmpPlugin):

    maptype = "CPUMap"
    modname = "ZenPacks.community.FujiMon.FujitsuCPU"
    relname = "cpus"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('hrProcessorTable',
                    '.1.3.6.1.2.1.25.3.3.1',
                    {
                        '.1': '_cpuidx',
                    }
        ),
        GetTableMap('cpuTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.30.1',
                    {
                        '.2': 'socket',
                        '.4': 'status',
                        '.5': 'setProductKey',
                        '.6': '_manuf',
                        '.8': 'clockspeed',
                        '.13': 'core',
                    }
        ),
        GetTableMap('cacheTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.40.1',
                    {
                        '.6': 'cpuidx',
                        '.11': 'level',
                        '.13': 'size',
                    }
        ),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cores = len(tabledata.get("hrProcessorTable", '')) / (len(tabledata.get(
                                                        "cpuTable", '1')) or 1)
        rm = self.relMap()
        cachemap = {}
        for cache in tabledata.get("cacheTable", {}).values():
            if cache['level'] < 3: continue
            if not cachemap.has_key(cache['cpuidx']):
                cachemap[cache['cpuidx']] = {}
            cachemap[cache['cpuidx']][cache['level']-2] = cache.get('size', 0)
        for oid, cpu in tabledata.get("cpuTable", {}).iteritems():
            om = self.objectMap(cpu)
            om.id = self.prepId("socket%s" % (om.socket))
            om.core = getattr(om, 'core', 0) or cores
            if not getattr(om, 'setProductKey', ''):
                om.setProductKey = 'Unknown Processor'
            om.setProductKey = MultiArgs(om.setProductKey.replace("(R)", ""),
                                        om.setProductKey.split()[0])
            for clevel, csize in cachemap[om.socket].iteritems():
                setattr(om, "cacheSizeL%d"%clevel, csize)
            rm.append(om)
        return rm

