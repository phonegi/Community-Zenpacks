################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Databases.

$Id: info.py,v 1.3 2010/09/28 16:18:47 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.community.RDBMS import interfaces


class DatabaseInfo(ComponentInfo):

    type = ProxyProperty("type")
    contact = ProxyProperty("contact")
    version = ProxyProperty("version")
    activeTime = ProxyProperty("activeTime")

    @property
    def name(self):
        return self._object.dbname

    @property
    @info
    def dbSrvInst(self):
        return self._object.getDBSrvInst()

    @property
    def blockSizeString(self):
        return self._object.blockSizeString()

    @property
    def totalBytesString(self):
        return self._object.totalString()

    @property
    def usedBytesString(self):
        return self._object.usedString()

    @property
    def availBytesString(self):
        return self._object.availString()

    @property
    def capacity(self):
        cap = self._object.capacity()
        if cap != 'Unknown': cap = '%s%%' % cap
        return cap

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class rdbmsDatabaseInfo(DatabaseInfo):
    implements(interfaces.IDatabaseInfo)

class DBSrvInstInfo(ComponentInfo):

    contact = ProxyProperty("contact")

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def name(self):
        return self._object.dbsiname

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()

class rdbmsDBSrvInstInfo(DBSrvInstInfo):
    implements(interfaces.IDBSrvInstInfo)

