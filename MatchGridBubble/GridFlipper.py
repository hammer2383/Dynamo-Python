# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
"""From Clockwork's Element.Category+"""

import System
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

views = UnwrapElement(IN[0])
grids = UnwrapElement(IN[1])
baseView = UnwrapElement(IN[2])

doc = DocumentManager.Instance.CurrentDBDocument

"""as the name suggest, it...flip...grid and also show/hide grid bubbles
4 modes (mode0-mode3) function represent each possible case for grid bubbles
this should prevent confusion of which end is start point or endpoint
"""

# (0,0)
def mode0(grid, view):
	grid.HideBubbleInView(DatumEnds.End1,view)
	grid.HideBubbleInView(DatumEnds.End0,view)
 
# (1,1)
def mode1(grid, view):		
	grid.ShowBubbleInView(DatumEnds.End1,view)
	grid.ShowBubbleInView(DatumEnds.End0,view)
 
# (1,0)
def mode2(grid, view):
    grid.ShowBubbleInView(DatumEnds.End0,view)
    grid.HideBubbleInView(DatumEnds.End1,view)

# (0,1)
def mode3(grid, view):
    grid.ShowBubbleInView(DatumEnds.End1,view)
    grid.HideBubbleInView(DatumEnds.End0,view)
  
  
# first is End0, sencond is End1
# mode 0 = (0,0)  mode 1 = (1,1)   mode 2 = (1,0)   mode 3 = (0,1)
def whichmode(grid, view):
    """Check what mode of the grid is in a view

    Args:
        grid (Revit Grid): Revit grid
        view (Revit view): Revit view, this suppose to be base view to set grid bubble for other view
        

    Returns:
        int: interger representation of mode
    """
    if grid.IsBubbleVisibleInView(DatumEnds.End0, view):
        if grid.IsBubbleVisibleInView(DatumEnds.End1, view):
            mode = 1            
        else:
            mode = 2            
    elif not grid.IsBubbleVisibleInView(DatumEnds.End0, view):
        if grid.IsBubbleVisibleInView(DatumEnds.End1, view):
            mode = 3            
        else:
            mode = 0            
            
    return mode


def setmode(mode,grid,view):
    """set mode of grid in a view

    Args:
        mode (int): interger representation of mode
        grid (Revit Grid): Revit grid
        view (Revit View): Revit view
    """
    if mode == 0:
        mode0(grid,view)
    elif mode == 1:
        mode1(grid,view)
    elif mode == 2:
        mode2(grid,view)
    elif mode == 3:
        mode3(grid,view)		
		
TransactionManager.Instance.EnsureInTransaction(doc)
for otherview in views:
    for grid in grids:
        try:
            basemode = whichmode(grid, baseView)
            setmode(basemode, grid, otherview)
        except:
            continue 
    

TransactionManager.Instance.TransactionTaskDone()