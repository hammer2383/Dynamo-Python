import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Line, Point, PolyCurve
# Import ToProtoType, ToRevitType geometry conversion extension methods
# Param:
#   CURVES(List)
#   TOPELE(Float)
#   BUTTELE(Float)
#   OFFSET(Float)
########################################################################
#-----------------------------------------------------------------------
CURVES = IN[0]
TOPELE = IN[1]
BUTTELE = IN[2]
OFFSET = IN[3]

def HorizonLine(curves):
    horizon_line = []    
    for c in curves:
        if c.StartPoint.Z == c.EndPoint.Z:
            horizon_line.append(c)

    return horizon_line

# Take 2 Horizon lines and compares
# return : (top, buttom) height
def GetTopAndButt(curves):
    horizon_lines = HorizonLine(curves)
    line1 = horizon_lines[0]
    line2 = horizon_lines[1] 
    if line1.StartPoint.Z > line2.StartPoint.Z:
        topandbutt = (line1.StartPoint.Z, line2.StartPoint.Z)
    else:
        topandbutt = (line2.StartPoint.Z, line1.StartPoint.Z)        
    return topandbutt

def GetTop(curves):
    horizon_lines = HorizonLine(curves)
    line1 = horizon_lines[0]
    line2 = horizon_lines[1] 
    if line1.StartPoint.Z > line2.StartPoint.Z:
        top = line1
    else:
        top = line2      
    return top

# Take list of curves and create new line base on input curves with new top and bottom values
def CreateNewLine(curves, newtop, newbottom):
    newlines = []
    topline = GetTop(curves)
    for c in curves:
        if c.StartPoint.Z != c.EndPoint.Z:
            sp = Point.ByCoordinates(c.StartPoint.X, c.StartPoint.Y, newtop)
            ep = Point.ByCoordinates(c.EndPoint.X, c.EndPoint.Y, newbottom)
        elif c.StartPoint.Z == c.EndPoint.Z and c == topline:
            sp = Point.ByCoordinates(c.StartPoint.X, c.StartPoint.Y, newtop)
            ep = Point.ByCoordinates(c.EndPoint.X, c.EndPoint.Y, newtop)
        elif c.StartPoint.Z == c.EndPoint.Z and c != topline:
            sp = Point.ByCoordinates(c.StartPoint.X, c.StartPoint.Y, newbottom)
            ep = Point.ByCoordinates(c.EndPoint.X, c.EndPoint.Y, newbottom)
        c_line = Line.ByStartPointEndPoint(sp, ep)
        newlines.append(c_line)    
    return newlines         

# Take list of curves and return list of modified one
def ModifyAll(curves_list):
    all_mod_curves = []
    show_curves = []
    for curves in curves_list:
        newline = CreateNewLine(curves, TOPELE + OFFSET, BUTTELE - OFFSET)
        joined_curves = PolyCurve.ByJoinedCurves(newline)
        show_curves.append(newline)
        all_mod_curves.append(joined_curves)
    return all_mod_curves, show_curves
 

OUT = ModifyAll(CURVES)