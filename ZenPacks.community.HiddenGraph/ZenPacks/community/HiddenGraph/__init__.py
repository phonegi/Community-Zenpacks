
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# monkeypatch GraphDef
from Products.ZenModel.GraphDefinition import GraphDefinition
setattr( GraphDefinition, 'visible', True )
GraphDefinition._properties += ( {'id':'visible', 'type':'boolean', 'mode':'w'}, )

# monkeypatch RRDView
def getDefaultGraphDefs(self, drange=None):
    """get the default graph list for this object"""
    graphs = []
    for template in self.getRRDTemplates():
        for g in template.getGraphDefs():
            
            # this line inserted to skip over graphs with visible property set to false
            if not g.visible: continue
            
            graph = {}
            graph['title'] = g.getId()
            try:
                graph['url'] = self.getGraphDefUrl(g, drange, template)
                graphs.append(graph)
            except ConfigurationError:
                pass
    return graphs

from Products.ZenModel.RRDView import RRDView
RRDView.getDefaultGraphDefs = getDefaultGraphDefs