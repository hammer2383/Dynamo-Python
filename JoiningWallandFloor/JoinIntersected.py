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

Matches = UnwrapElement(IN[0])

# This one won't be use yet
# Check if elements are joined?
def IsJoinAtAll(document, main_element, second_element):
	return db.JoinGeometryUtils.AreElementsJoined(document, main_element, second_element)

# Joinging 2 elements
# main_element: cutting element
# second_element : cutted element
def JoiningElements(document, main_element, second_element):
		db.JoinGeometryUtils.JoinGeometry(document, main_element, second_element)
	
doc = DocumentManager.Instance.CurrentDBDocument
TransactionManager.Instance.EnsureInTransaction(doc)
for match in Matches:
    wall = match[0]
    floors = match[1]
    for floor in floors:
        JoiningElements(doc, wall, floor)    
TransactionManager.Instance.TransactionTaskDone()
OUT = Matches