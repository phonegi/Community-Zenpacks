################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellDiscreteTemperatureSensor

DellDiscreteTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: DellDiscreteTemperatureSensor.py,v 1.2 2010/06/30 21:54:15 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.TemperatureSensor import *
from DellComponent import *

class DellDiscreteTemperatureSensor(TemperatureSensor, DellComponent):
    """Discrete TemperatureSensor object"""

    threshold = 1
    status = 1

    _properties = TemperatureSensor._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                )

    def temperatureCelsiusString(self):
        """
        Return the current discrete temperature as a string
        """
        tempC = self.temperatureCelsius()
        if tempC == 1: return "Good"
        if tempC == 2: return "Bad"
        return "Unknown"

    def temperatureFahrenheitString(self):
        """
        Return the current discrete temperature as a string
        """
        return self.temperatureCelsiusString()

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break

    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
                     )

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellDiscreteTemperatureSensor)
