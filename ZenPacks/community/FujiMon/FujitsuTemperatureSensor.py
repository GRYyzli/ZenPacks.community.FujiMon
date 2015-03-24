################################################################################
#
# This program is part of the FujitsuMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.ZenModel.TemperatureSensor import *
from FujitsuComponent import *


class FujitsuTemperatureSensor(TemperatureSensor, FujitsuComponent):

    threshold = 0
    status = 1

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Unknown'),
                2: (DOT_GREY, SEV_WARNING, 'not-available'),
                3: (DOT_GREEN, SEV_CLEAN, 'ok'),
                4: (DOT_RED, SEV_CRITICAL, 'sensor-failed'),
                5: (DOT_RED, SEV_CRITICAL, 'failed'),
                6: (DOT_RED, SEV_CRITICAL, 'temperature-warning-toohot'),
                7: (DOT_RED, SEV_CRITICAL, 'temperature-critical-toohot'),
                8: (DOT_GREEN, SEV_CLEAN, 'temperature-normal'),
                9: (DOT_RED, SEV_CRITICAL, ' temperature-warning'),
                }


    _properties = TemperatureSensor._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                )

    def temperatureCelsius(self, default=None):
	
        tempC = self.cacheRRDValue('temperature_celsius', 0)
        if tempC is not None:
            return long(tempC)
        return None
    temperature = temperatureCelsius

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break

    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
                    )

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(FujitsuTemperatureSensor)
