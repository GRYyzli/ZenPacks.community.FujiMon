################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.CPU import *

class FujitsuCPU(CPU):

    core = 1
    socket = 0
    clockspeed = 0
    extspeed = 0
    voltage = 0
    cacheSizeL1 = 0
    cacheSizeL2 = 0
    cacheSizeL3 = 0
    status = 1

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Unknown'),
                2: (DOT_ORANGE, SEV_ERROR, 'not-present'),
                3: (DOT_GREEN, SEV_CLEAN, 'OK'),
                4: (DOT_GREEN, SEV_CLEAN, 'disabled'),
                5: (DOT_RED, SEV_CRITICAL, 'error'),
                6: (DOT_RED, SEV_CRITICAL, 'failed'),
                7: (DOT_ORANGE, SEV_ERROR, 'missing-termination'),
                8: (DOT_RED, SEV_CRITICAL, 'prefailure-warning'),
    }

    _properties = (
         {'id':'core', 'type':'int', 'mode':'w'},
         {'id':'socket', 'type':'int', 'mode':'w'},
         {'id':'clockspeed', 'type':'int', 'mode':'w'}, 
         {'id':'extspeed', 'type':'int', 'mode':'w'}, 
         {'id':'voltage', 'type':'int', 'mode':'w'}, 
         {'id':'cacheSizeL1', 'type':'int', 'mode':'w'}, 
         {'id':'cacheSizeL2', 'type':'int', 'mode':'w'}, 
         {'id':'cacheSizeL3', 'type':'int', 'mode':'w'}, 
    )

InitializeClass(FujitsuCPU)
