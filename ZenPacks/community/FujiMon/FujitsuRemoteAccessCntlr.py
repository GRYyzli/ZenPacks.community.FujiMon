################################################################################
#
# This program is part of the FujitsuMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from FujitsuExpansionCard import *

class FujitsuRemoteAccessCntlr(FujitsuExpansionCard):

    FWRev = ""
    SWVer = ""
    ipaddress = ""
    macaddress = ""
    subnetmask = ""

    # we monitor DRAC Controllers
    monitor = True

    _properties = FujitsuExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'SWVer', 'type':'string', 'mode':'w'},
        {'id':'ipaddress', 'type':'string', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'subnetmask', 'type':'string', 'mode':'w'},
    )


    factory_type_information = (
        {
            'id'             : 'FujitsuRemoteAccessCntlr',
            'meta_type'      : 'FujitsuRemoteAccessCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addFujitsuRemoteAccessCntlr',
            'immediate_view' : 'viewFujitsuRemoteAccessCntlr',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewFujitsuRemoteAccessCntlr'
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

    def getDeviceProductName(self):
        return self.device().hw.getProductName()

    def getDeviceProductLink(self):
        return self.device().hw.getProductLink()

InitializeClass(FujitsuRemoteAccessCntlr)
