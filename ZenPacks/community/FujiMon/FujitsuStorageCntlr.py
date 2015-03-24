################################################################################
#
# This program is part of the FujitsuMon Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenUtils.Utils import convToUnits
from FujitsuExpansionCard import *

class FujitsuStorageCntlr(FujitsuExpansionCard):

    FWRev = ""
    SWVer = ""
    role = 1
    cacheSize = 0
    controllerType = ""

    monitor = True
    
    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREY, SEV_WARNING, 'Unknown'),
                3: (DOT_GREEN, SEV_CLEAN, 'Ready/OK'),
                4: (DOT_YELLOW, SEV_WARNING, 'Non-critical'),
                5: (DOT_ORANGE, SEV_ERROR, 'Critical'),
                6: (DOT_RED, SEV_CRITICAL, 'Non-recoverable'),
                }

    _properties = FujitsuExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'SWVer', 'type':'string', 'mode':'w'},
        {'id':'role', 'type':'int', 'mode':'w'},
        {'id':'cacheSize', 'type':'int', 'mode':'w'},
        {'id':'controllerType', 'type':'string', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'FujitsuStorageCntlr',
            'meta_type'      : 'FujitsuStorageCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addFujitsuStorageCntlr',
            'immediate_view' : 'viewFujitsuStorageCntlr',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewFujitsuStorageCntlr'
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

    def roleString(self):
        
	roles = {1: 'Enables',
                2: 'Disabled',
                3: 'Active',
                99: 'Not Applicable',
                }
        return roles.get(self.role, roles[99])

    def cacheSizeString(self):
        
	return convToUnits(self.cacheSize)

InitializeClass(FujitsuStorageCntlr)
