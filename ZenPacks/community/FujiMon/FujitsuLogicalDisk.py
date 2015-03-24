################################################################################
#
# This program is part of the FujitsuMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from ZenPacks.community.deviceAdvDetail.LogicalDisk import *
from FujitsuComponent import *

class FujitsuLogicalDisk(LogicalDisk, FujitsuComponent):

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Unknown'),
                2: (DOT_GREEN, SEV_CLEAN, 'Operational'),
                3: (DOT_RED, SEV_CRITICAL, 'PartiallyDegraded'),
                4: (DOT_GREEN, SEV_CRITICAL, 'Degraded'),
                5: (DOT_RED, SEV_CRITICAL, 'Failed'),
                6: (DOT_ORANGE, SEV_WARNING, 'Rrebuilding'),
                7: (DOT_YELLOW, SEV_WARNING, 'Checking'),
                8: (DOT_ORANGE, SEV_ERROR, 'Mdcing'),
                9: (DOT_YELLOW, SEV_WARNING, 'Initializing'),
                10: (DOT_YELLOW, SEV_WARNING, 'BackgroundInitializing'),
                11: (DOT_YELLOW, SEV_WARNING, 'Migrating'),
                12: (DOT_YELLOW, SEV_WARNING, 'Copying'),
                13: (DOT_YELLOW, SEV_WARNING, 'Offline'),
                14: (DOT_ORANGE, SEV_WARNING, 'SpareInUse'),
                15: (DOT_YELLOW, SEV_WARNING, 'Erasing'),
                }


    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewFujitsuLogicalDisk',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewFujitsuLogicalDisk'
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
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(FujitsuLogicalDisk)
