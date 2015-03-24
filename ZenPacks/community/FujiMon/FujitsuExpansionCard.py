################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.ExpansionCard import *
from FujitsuComponent import *

class FujitsuExpansionCard(ExpansionCard, FujitsuComponent):

    slot = 0
    status = 1
    monitor = False

    _properties = HWComponent._properties + (
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'FujitsuExpansionCard',
            'meta_type'      : 'FujitsuExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'FujitsuMon',
            'factory'        : 'manage_addDellExpansionCard',
            'immediate_view' : 'viewFujitsuExpansionCard',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellExpansionCard'
                , 'permissions'   : (ZEN_VIEW,)
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
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(FujitsuExpansionCard)
