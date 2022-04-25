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


# Code here

ElementsToBeCut = UnwrapElement(IN[0])
CuttingElements = UnwrapElement(IN[1])
Matches = zip(ElementsToBeCut, CuttingElements)


# This one won't be use yet
# Check if elements are joined?
def IsJoinAtAll(document, main_element, second_element):
	return db.JoinGeometryUtils.AreElementsJoined(document, main_element, second_element)

# Joinging 2 elements
# main_element: cutting element
# second_element : cutted element
def ToCutElements(document, SolidToBeCut, CuttingSolid):
		try:
			db.SolidSolidCutUtils.AddCutBetweenSolids(document, SolidToBeCut, CuttingSolid)
		except:
			pass
	

doc = DocumentManager.Instance.CurrentDBDocument
TransactionManager.Instance.EnsureInTransaction(doc)

for match in Matches:
	for tobecut in match[0]:
		ToCutElements(doc, tobecut, match[1])    
    
TransactionManager.Instance.TransactionTaskDone()

OUT = Matches