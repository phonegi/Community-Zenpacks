################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPCPUMap

HPCPUMap maps the cpqSeCpuTable and cpqSeCpuCacheTable tables to cpu objects

$Id: HPCPUMap.py,v 1.3 2009/08/18 16:37:53 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPCPUMap(SnmpPlugin):
    """Map HP/Compaq insight manager cpu table to model."""

    maptype = "HPCPUMap"
    modname = "ZenPacks.community.HPMon.HPCPU"
    relname = "cpus"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('hrProcessorTable',
                    '.1.3.6.1.2.1.25.3.3.1',
                    {
                        '.1': '_cpuidx',
                    }
        ),
        GetTableMap('cpuTable',
                    '.1.3.6.1.4.1.232.1.2.2.1.1',
                    {
                        '.1': '_cpuidx',
                        '.3': 'setProductKey',
                        '.4': 'clockspeed',
                        '.5': 'null',
                        '.6': 'null',
                        '.7': 'extspeed',
                        '.8': 'null',
                        '.9': 'socket',
                        '.15':'core',
            }
        ),
        GetTableMap('cacheTable',
                    '.1.3.6.1.4.1.232.1.2.2.3.1',
                    {
                        '.1': 'cpuidx',
                        '.2': 'level',
                        '.3': 'size',
                    }
        ),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cputable = tabledata.get("cpuTable")
        cachetable = tabledata.get("cacheTable")
        if not cputable: return
        cores = len(tabledata.get("hrProcessorTable")) / len(cputable)
        if cores == 0: cores = 1
        rm = self.relMap()
        cpumap = {}
        cachemap = {}
        if cachetable:
            for cache in cachetable.values():
                if not cachemap.get(cache['cpuidx']):cachemap[cache['cpuidx']]={}
                cachemap[cache['cpuidx']][cache['level']] = cache.get('size',0)
        for cpu in cputable.values():
            del cpu['null']
            om = self.objectMap(cpu)
            idx = getattr(om, 'socket', om._cpuidx)
            om.id = self.prepId("%s_%s" % (om.setProductKey,idx))
            om.core = getattr(om, 'core', 0)
            if om.core == 0: om.core = cores
            for level, size in cachemap[om._cpuidx].iteritems():
                setattr(om, "cacheSizeL%d"%level, size)
            rm.append(om)
        return rm
