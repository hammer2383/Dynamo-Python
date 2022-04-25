import clr
import System
import operator
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
import Autodesk.Revit.DB as db

############################
#########CODE HERE##########
############################
#   Copy below dash
#---------------------------
# Param:
#   FOLDER: List of folder name in string
#   EXCEPTVIEW: List of view name in string
#   VIEWS: List of view(Revit elements)
#   DoDelete: Boolean True to delete views
FOLDER = IN[0]
EXCEPTVIEW = IN[1]
VIEWS = UnwrapElement(IN[2])
DoDELETE = IN[3]

# Check if particular views is an exception
# Check for folder first then specific view name
def IsAnException(infolders, inexceptedviews, view):
    """return True if view is in exception condition"""
    if view.LookupParameter("Folder").AsString() in infolders:
        return True
    else:
        if view.LookupParameter("View Name").AsString() in inexceptedviews:
            return True
        else:
            return False

def DeleteElement(RevitElements):    
    doc.Delete(RevitElements.Id)

### Doc transaction start ###
doc = DocumentManager.Instance.CurrentDBDocument
TransactionManager.Instance.EnsureInTransaction(doc)

# Apply filter
Exclude = [v for v in VIEWS if IsAnException(FOLDER, EXCEPTVIEW, v) is True] # view that won't be delete
NonExcept = [v for v in VIEWS if IsAnException(FOLDER, EXCEPTVIEW, v) is False] # view to be delete


# Get any parent view #
FirstExcluded = UnwrapElement(IN[4]) # all excluded element from GetAllView module
FirstExcluded = [e for e in FirstExcluded] # copy
Exclude = Exclude + FirstExcluded # merged all view that won't be delete

"""Exclude parent view from ToDeleteView, or else Revit will delete dependent view.
"""
ToDeleteView = NonExcept[:] # copy list
for eview in Exclude:
    try:
        parentviewId =  eview.LookupParameter("Parent View").AsElementId()    
        for pview in NonExcept:
            if pview.Id == parentviewId:
                ToDeleteView.remove(pview)
    except:
        continue    
DeletedViewsName = [v.LookupParameter("View Name").AsString() for v in ToDeleteView]  # just for Watch ouput
# Start Delete View
if DoDELETE:    
    for v in ToDeleteView:
        if v.IsValidObject:                       
            DeleteElement(v)
        else:
            continue        
    OUT = DeletedViewsName
else:
    OUT = ToDeleteView

TransactionManager.Instance.TransactionTaskDone()
### Doc transaction end ###


        