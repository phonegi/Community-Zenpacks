################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellComponent

DellComponent is an abstraction

$Id: DellComponent.py,v 1.0 2009/06/23 00:36:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.HWStatus import *

class DellComponent(HWStatus):

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREY, SEV_WARNING, 'Unknown'),
                3: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                4: (DOT_YELLOW, SEV_WARNING, 'Non Critical Upper'),
                5: (DOT_ORANGE, SEV_ERROR, 'Critical Upper'),
                6: (DOT_RED, SEV_CRITICAL, 'Non Recoverable Upper'),
                7: (DOT_YELLOW, SEV_WARNING, 'Non Critical Lower'),
                8: (DOT_ORANGE, SEV_ERROR, 'Critical Lower'),
                9: (DOT_RED, SEV_CRITICAL, 'Non Recoverable Lower'),
                10: (DOT_RED, SEV_CRITICAL, 'Failed'),
                }
