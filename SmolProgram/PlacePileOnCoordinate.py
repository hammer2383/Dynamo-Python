# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitAPI")
from Autodesk.DesignScript import Geometry
from Autodesk.Revit.DB import XYZ


# The inputs to this node will be stored as a list in the IN variables.
NSCoords = IN[0][0][11:]
EWCoords = IN[0][1][11:]
pileMark = IN[0][2][11:]


def CheckEmpty(coord):
    if coord == " ":
        return False
    else:
        return True
NSCoords = list(filter(CheckEmpty, NSCoords))
EWCoords = list(filter(CheckEmpty, EWCoords))
pileMark = list(filter(CheckEmpty, pileMark))

SurveyCoords = zip(EWCoords, NSCoords)



def PointFromCoordinates(EW, NS):
    return Geometry.Point.ByCoordinates(EW, NS)

pointsList = []
for sc in SurveyCoords:
    EWCoord = sc[0]
    NSCoord = sc[1]
    point = PointFromCoordinates(EWCoord, NSCoord)
    pointsList.append(point)


OUT = pointsList, pileMark