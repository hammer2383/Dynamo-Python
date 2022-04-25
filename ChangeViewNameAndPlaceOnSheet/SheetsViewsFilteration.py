import clr

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

"""
This program will get sheets and views that met these criteria;
    For sheet
    1. doesn't have any viewport on sheet
    2. the view name must contain specific string which user defined
    For views(MAGICWORD)
    1. are not Schedule or Legend view or View template
    2. not already on sheet
    3. the view name must contain specific string which user defined
    4. Is in specific Folder
    
"""




##CODE START HERE##
collector = FilteredElementCollector(doc)
views = collector.OfClass(View).ToElements()

viewlist = [] # list of view that's View
sheetlist = []
MAGICWORD = IN[0] # specfic strings which defined by user
FOLDER = IN[1]

# get sheet that doesn't have any viewport on sheet
for v in views:
    try:
        if v.Category.Name == "Sheets":        	
            if not v.GetAllPlacedViews():
                sheetlist.append(v)
        else:
            continue
    except:
        continue

# get view
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
  
# get view not already on sheet

ViewNotOnSheet = [v for v in viewlist if v.LookupParameter("Sheet Name") is None and v.LookupParameter("Folder").AsString() == FOLDER]


def IsInName(v, serchfor):
    return serchfor in v.ViewName

filteredviews = [v for v in ViewNotOnSheet if IsInName(v,MAGICWORD) is True]
filteredsheets = [v for v in sheetlist if IsInName(v,MAGICWORD) is True]

OUT = filteredviews, filteredsheets