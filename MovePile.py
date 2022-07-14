# Move existing foundation pile into specific location (it will also work with most family instance)
# import sys
# from xml.dom.minidom import Element
import clr
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitAPI")
clr.AddReference("RevitNodes")

clr.AddReference("RevitServices")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
from Autodesk.DesignScript.Geometry import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from Autodesk.Revit.DB import XYZ

doc = DocumentManager.Instance.CurrentDBDocument

pilePoints = UnwrapElement(IN[0]) # geometry point
marks = IN[1] # piles' mark
piles = UnwrapElement(IN[2]) # Revit foundation piles 

MARKPILEPOINT = zip(marks, pilePoints) # Data from excel, list of piles' mark and geometry point. i.e. [[PW1, Point]]

# Get pile mark to use with data from excel (MARKPILEPOINT).
def GetPileMark(pile):
    markParam = pile.GetParameters("Mark")
    markParam = markParam[0]
    pileMark = markParam.AsString()
    return pileMark

# Create new point.
def PointFromMark(pile):
    """Create Revit Point by find the matching pile mark from pile element with pile mark in MARKPILEPOINT.
    Z value would be the same as existing pile location.

    Args:
        pile (Revit Element): Revit family instance

    Returns:
        Revit Point: New revit point in which the pile while relocate to.
    """
    for mark in MARKPILEPOINT:
        if mark[0] == GetPileMark(pile):
            pilePoint = mark[1]
            #Create new point with Z value from pile's location
            pileRevitPoint = pilePoint.ToXyz()
            newPilePoint = XYZ(pileRevitPoint.X, pileRevitPoint.Y, pile.Location.Point.Z)

            return newPilePoint

        else:
            continue  




TransactionManager.Instance.EnsureInTransaction(doc)

# Change piles to the location.
for p in piles:
    newPoint = PointFromMark(p)
    p.Location.Point = newPoint


TransactionManager.Instance.TransactionTaskDone()
OUT = piles

