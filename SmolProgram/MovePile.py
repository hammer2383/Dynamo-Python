# Load the Python Standard and DesignScript Libraries
import sys
from xml.dom.minidom import Element
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

pilePoints = UnwrapElement(IN[0])
marks = IN[1]
piles = UnwrapElement(IN[2])

MARKPILEPOINT = zip(marks, pilePoints)

#Get pile mark
def GetPileMark(pile):
    markParam = pile.GetParameters("Mark")
    markParam = markParam[0]
    pileMark = markParam.AsString()
    return pileMark

#Find point from mark
def PointFromMark(pile):
    for mark in MARKPILEPOINT:
        if mark[0] == GetPileMark(pile):
            pilePoint = mark[1]

            #Create new point with Z value from pile
            pileRevitPoint = pilePoint.ToXyz()
            newPilePoint = XYZ(pileRevitPoint.X, pileRevitPoint.Y, pile.Location.Point.Z)

            return newPilePoint

        else:
            continue  




TransactionManager.Instance.EnsureInTransaction(doc)
#element1.Location.Point = revitPoint
for p in piles:
    newPoint = PointFromMark(p)
    p.Location.Point = newPoint


TransactionManager.Instance.TransactionTaskDone()
OUT = piles

