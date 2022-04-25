
from os import pardir
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)


collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElements()
viewlist = []
viewname = []
folder = IN[0]
def IsAnException(infolders, view):
    """return True if view is in exception condition"""
    param = view.LookupParameter("Folder")
#    if param.AsString() in infolders:
    if param.AsString() in infolders:
        return True
    else:
        return False
r = []        
for v in views:  
    if not hasattr(v.Category, "Name"):
        continue
    
    rule = [v.IsTemplate is False,
            v.Category.Name != "Sheets",
            v.Category.Name != "Schedules",
            str(v.ViewType) != "Legend"]    
    if all(rule):      
        try:    	
            if IsAnException(folder, v):                        
                    viewlist.append(v)
                    viewname.append(v.Name)
        except:
            param = v.LookupParameter("Folder")
            param = param.AsString()                     
            er = ["er",v]        
            
  
OUT = viewname, viewlist