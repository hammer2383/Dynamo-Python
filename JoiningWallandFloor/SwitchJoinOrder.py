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

### Code started here ###

# This script will switch joining order of elements
# it only switch order if joined elements are floor category

Matches = UnwrapElement(IN[0]) # list's structre: [wall,[floor1,floor2],....,]
SWITCH_JOINING = IN[1] # Boolean: should main() be execute?

# Check if main_element is a cutting element
# return True if main_element is a cutting element
def CuttingOrder(document, main_element, second_element):
	return db.JoinGeometryUtils.IsCuttingElementInJoin(document, main_element, second_element)

# Switch improper elements joining order between an element and floor.
# param:
#   is_proper : boolean, if value is False the function will switch elements order.
def properSwitchOfElements(document, is_proper, main_element, joined_element):
    if joined_element.Category.Name == "Floors":
        if is_proper:
            pass
        else:
            try:
                db.JoinGeometryUtils.SwitchJoinOrder(document, main_element, joined_element)
            except:
                pass
    else:
        pass

def main():
    doc = DocumentManager.Instance.CurrentDBDocument
    TransactionManager.Instance.EnsureInTransaction(doc)
    for match in Matches:
        wall = match[0]
        floors = match[1]
        for floor in floors:
            is_proper = CuttingOrder(doc, wall, floor)
            properSwitchOfElements(doc, is_proper, wall, floor) 

    TransactionManager.Instance.TransactionTaskDone()

if SWITCH_JOINING:
	main()
OUT = Matches