# code from MEPover
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import clr
clr.AddReference('RevitAPI')
import Autodesk.Revit.DB

import clr
clr.AddReference("RevitNodes")
import Revit

clr.AddReference('DSCoreNodes')
import DSCore
from DSCore import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

#The inputs to this node will be stored as a list in the IN variables.
if isinstance(IN[0], list):
	views = UnwrapElement(IN[0])
else:
	views = [UnwrapElement(IN[0])]
if isinstance(IN[1], list):
	if IN[1][0].GetType() == PolyCurve:
		curves = [PolyCurve.Curves(x) for x in IN[1]]
	elif IN[1][0].GetType() == Curve or IN[1][0].GetType() == Line:
		curves = List.OfRepeatedItem(IN[1],len(views))
	else:
		curves = IN[1]
else:
	if IN[1].GetType() == PolyCurve:
		curves = [PolyCurve.Curves(IN[1])]
	else:
		curves = [IN[1]]
	
listout = []
for view,curve in zip(views,curves):
	regionMan = view.GetCropRegionShapeManager()
	revit_curve = [c.ToRevitType() for c in curve]
	curveloop = Autodesk.Revit.DB.CurveLoop()
	for c in revit_curve:
		curveloop.Append(c)
	TransactionManager.Instance.EnsureInTransaction(doc)
	if view.CropBoxActive == False:
		view.CropBoxActive = True
		view.CropBoxVisible = True
	regionMan.SetCropShape(curveloop)
	TransactionManager.Instance.TransactionTaskDone()
	listout.append(view)


#Assign your output to the OUT variable.
OUT = listout