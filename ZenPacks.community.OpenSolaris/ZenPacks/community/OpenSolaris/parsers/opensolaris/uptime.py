###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################


import re
import logging

from Products.ZenRRD.CommandParser import CommandParser


log = logging.getLogger("zen.zencommand")


UPTIME_PATTERN = re.compile(
    r"up +(?:(?P<days>\d+) days?, +)?(?:(?P<hours>\d+):)?(?P<minutes>\d+)")

UPTIME_FORMAT = "uptime: days=%(days)s, hours=%(hours)s, minutes=%(minutes)s"


def parseUptime(output):
    """
    Parse the uptime command's output capturing the days, hours and minutes
    that the system has been up. Returns a dictionary of the captured values.
    
    >>> UPTIME_FORMAT % parseUptime("up 1 day, 1:42")
    'uptime: days=1, hours=1, minutes=42'
    
    >>> UPTIME_FORMAT % parseUptime("up 5 days, 1:42")
    'uptime: days=5, hours=1, minutes=42'
    
    >>> UPTIME_FORMAT % parseUptime("up 3 days, 6 min")
    'uptime: days=3, hours=0, minutes=6'
    
    >>> UPTIME_FORMAT % parseUptime("up 1:14")
    'uptime: days=0, hours=1, minutes=14'
    
    >>> UPTIME_FORMAT % parseUptime("up 4 min")
    'uptime: days=0, hours=0, minutes=4'
    
    """
    
    match = UPTIME_PATTERN.search(output)
    
    if match:
        uptime = dict([(k, int(v)) for k, v in match.groupdict(0).items()])
        log.debug(UPTIME_FORMAT % uptime)
    else:
        uptime = None
        log.debug("uptime: no match")
        
    return uptime
    
    
def asTimeticks(days=0, hours=0, minutes=0):
    return ((days * 24 + hours) * 60 + minutes) * 60 * 100
    
    
def parseSysUpTime(output):
    """
    Parse the sysUpTime (measured in timeticks) from the output of the uptime
    command.    
    """
    uptime = parseUptime(output)
    
    if uptime: sysUpTime = asTimeticks(**uptime)
    else     : sysUpTime = None
    
    return sysUpTime
    
    
class uptime(CommandParser):
    
    
    def processResults(self, cmd, result):
        """
        Parse the results of the uptime command to get sysUptime and load
        averages.
        """
        output = cmd.result.output
        
        dps = dict([(dp.id, dp) for dp in cmd.points])

        if 'sysUpTime' in dps:
            sysUpTime = parseSysUpTime(output)
            if sysUpTime:
                result.values.append((dps['sysUpTime'], sysUpTime))
                
        match = re.search(r' load averages?: '
                          r'([0-9.]+),? ([0-9.]+),? ([0-9.]+)$',
                          output)
        if match:
            for i, dp in enumerate(['laLoadInt1', 'laLoadInt5', 'laLoadInt15']):
                if dp in dps:
                    result.values.append( (dps[dp], float(match.group(i + 1))) )
        return result
