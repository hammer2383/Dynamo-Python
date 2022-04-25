import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)


##CODE START HERE##
#collect all views in the model excludes: Sheets, Empty Category View

collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElements()

viewlist = [] # list of view that's View
keeplist = [] # list of view to keep
#get atleast one sheet
for v in views:
    try:
        if v.Category.Name == "Sheets":
            sheetview = v
            break
        else:
            continue
    except:
        continue

for i in views:
    try:
        if not i.IsTemplate and not i.Category.Name == "Sheets" and not i.Category.Name == "Schedules" and not str(i.ViewType) == "Legend":
            if i != None:
                viewlist.append(i)
            else:
                continue
        else:            
           	continue
    except:
        continue	
###
#eview = UnwrapElement(IN[1])
#OUT = eview.LookupParameter("Parent View").AsElementId()
#Assign your output to the OUT variable
OUT = [[v for v in viewlist if v.LookupParameter("Sheet Name") is None],
		sheetview,
		[v for v in viewlist if v.LookupParameter("Sheet Name") is not None]]