
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

"""Get only view that're not Sheets, Schedules, Legend.
    viewname only needed for Keys_ input of Data-Shapes node for clean looking UI

    OUT:
        Tuple: List of viewname(str), List of view(Revit view)
"""

collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElements() # get all views
viewlist = [] # List of revit view
viewname = [] # List of view name are for Keys_ input of Data-Shapes node
folder = IN[0] # Folder name(string)

def IsAnException(folder, view):
    """Check if view is in specific Folder"""
    param = view.LookupParameter("Folder")
    # if param.AsString() in infolders:
    if param.AsString() in folder:
        return True
    else:
        return False


# Filter out View that are Sheets, Schedules, Legend and aren't in specific folder     
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
            continue        
            
  
OUT = viewname, viewlist