################################################################################
#
# This program is part of the FujitsuMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import inspect
from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.HardDisk import *
from FujitsuComponent import *

class FujitsuHardDisk(HardDisk, FujitsuComponent):

    rpm = 0
    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""
    status = 1

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Unknown'),
                2: (DOT_GREEN, SEV_CLEAN, 'noDisk'),
                3: (DOT_GREEN, SEV_CLEAN, 'available'),
                4: (DOT_GREEN, SEV_CLEAN, 'operational'),
                5: (DOT_RED, SEV_CRITICAL, 'failed'), 
                6: (DOT_ORANGE, SEV_ERROR, 'rebuilding'),
                7: (DOT_GREEN, SEV_CLEAN, 'globalHotSpare'),
                8: (DOT_GREEN, SEV_CLEAN, 'dedicatedHotSpare'),
                9: (DOT_RED, SEV_CRITICAL, 'offline'),
                10: (DOT_RED, SEV_CRITICAL, 'unconfiguredFailed'),
                11: (DOT_RED, SEV_CRITICAL, 'failedMissing'),
                12: (DOT_ORANGE, SEV_ERROR, 'copyBack'),
                13: (DOT_ORANGE, SEV_WARNING, 'redundantCopy'),
                14: (DOT_ORANGE, SEV_WARNING, 'waiting'),
                15: (DOT_ORANGE, SEV_WARNING, 'preparing'),
                16: (DOT_ORANGE, SEV_WARNING, 'migrating'),
                17: (DOT_ORANGE, SEV_WARNING, 'jbod'),
                18: (DOT_ORANGE, SEV_WARNING, 'shielded'),
                19: (DOT_ORANGE, SEV_WARNING, 'clearing'),
                20: (DOT_ORANGE, SEV_WARNING, 'erasing'),
                }


    _properties = HardDisk._properties + (
                 {'id':'rpm', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                 {'id':'status', 'type':'int', 'mode':'w'},
                )

    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewFujitsuHardDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewFujitsuHardDisk'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    def sizeString(self):
        
	return convToUnits(self.size,divby=1000)

    def rpmString(self):
        
	if int(self.rpm) == 1:
            return 'Unknown'
        if int(self.rpm) < 10000:
            return int(self.rpm)
        else:
            return "%sK" %(int(self.rpm) / 1000)

    def getRRDTemplates(self):
        
	templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(FujitsuHardDisk)
