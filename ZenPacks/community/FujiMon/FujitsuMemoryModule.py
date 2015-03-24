################################################################################
#
# This program is part of the FujitsuMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from ZenPacks.community.deviceAdvDetail.MemoryModule import *
from FujitsuComponent import *

class FujitsuMemoryModule(MemoryModule, FujitsuComponent):

    status = 1
    speed = ""

    _properties = MemoryModule._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
        {'id':'speed', 'type':'string', 'mode':'w'},
    )

    def speedString(self):
        
	return self.speed

    def getRRDTemplates(self):
        
	templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(FujitsuMemoryModule)
