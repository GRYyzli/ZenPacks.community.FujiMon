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
from Products.ZenModel.PowerSupply import *
from FujitsuComponent import *

class FujitsuPowerSupply(PowerSupply, FujitsuComponent):

    state = property(fget=lambda self: self.statusString())
    status = 1
    volts = 0
    vpsnmpindex = ""
    vptype = 0
    apsnmpindex = ""
    aptype = 0
    __snmpindex = ""

    statusmap ={1: (DOT_ORANGE, SEV_ERROR, 'Unknown'),
                2: (DOT_ORANGE, SEV_ERROR, 'Not-present'),
                3: (DOT_GREEN, SEV_CLEAN, 'OK'),
                4: (DOT_RED, SEV_CRITICAL, 'Failed'),
                5: (DOT_RED, SEV_CRITICAL, 'AC Fail'),
                6: (DOT_RED, SEV_CRITICAL, 'DC Fail'),
                7: (DOT_RED, SEV_CRITICAL, 'Critical-temperature'),
                8: (DOT_RED, SEV_CRITICAL, 'Not-manageable'),
                9: (DOT_RED, SEV_CRITICAL, 'Fan-failure-predicted'),
                10:(DOT_RED, SEV_CRITICAL, 'Fan-failure'),
                11:(DOT_RED, SEV_CRITICAL, 'Power-safe-mode'),
                12:(DOT_RED, SEV_CRITICAL, 'Non-redundant-dc-fail'),
                13:(DOT_RED, SEV_CRITICAL, 'Non-redundant-ac-fail'),
                }

    _properties = PowerSupply._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    @property
    def state(self):
        return self.statusString()

    _properties = PowerSupply._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'PowerSupply',
            'meta_type'      : 'PowerSupply',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'PowerSupply_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPowerSupply',
            'immediate_view' : 'viewFujitsuPowerSupply',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewFujitsuPowerSupply'
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

    def getRRDTemplates(self):
        
	templates = []
        tnames = ['FujitsuPowerSupply',]
        for tname in tnames:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

    def _setSnmpIndex(self, value):
        
	self.__snmpindex = value

    snmpindex = property(fget=lambda self: self._getSnmpIndex(),
                        fset=lambda self, v: self._setSnmpIndex(v)
                        )

    def setState(self, value):
        
	self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break

    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
                     )

InitializeClass(FujitsuPowerSupply)
