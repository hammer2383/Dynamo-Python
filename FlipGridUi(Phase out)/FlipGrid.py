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

UseActiveView = IN[0]
view = UnwrapElement(IN[1])
GRID = UnwrapElement(IN[2])
mode = IN[3]

doc = DocumentManager.Instance.CurrentDBDocument

# show both end (2)
def onbothend(grid, view):		
	grid.ShowBubbleInView(DatumEnds.End1,v)
	grid.ShowBubbleInView(DatumEnds.End0,v)

# off both end (0)
def offbothend(grid, view):
	grid.HideBubbleInView(DatumEnds.End1,v)
	grid.HideBubbleInView(DatumEnds.End0,v)

# one end and switch end(1)
def oneend(grid, view):
	if grid.IsBubbleVisibleInView(DatumEnds.End0,v):
		grid.HideBubbleInView(DatumEnds.End0,v)
		grid.ShowBubbleInView(DatumEnds.End1,v)		
	elif grid.IsBubbleVisibleInView(DatumEnds.End1,v):
		grid.HideBubbleInView(DatumEnds.End1,v)
		grid.ShowBubbleInView(DatumEnds.End0,v)		
	else:
		grid.ShowBubbleInView(DatumEnds.End0,v)		
def changebubble(grid, view, mode):
	if mode == "0":
		offbothend(grid,v)
	elif mode == "2":
		onbothend(grid,v)
	elif mode == "1":
		oneend(grid,v)
		
TransactionManager.Instance.EnsureInTransaction(doc)
if UseActiveView:
	for g in GRID:
		activeview = doc.ActiveView
		changebubble(g,activeview,mode)	
else:
	for g in GRID:
		for v in view:
			changebubble(g,v,mode)

TransactionManager.Instance.TransactionTaskDone()