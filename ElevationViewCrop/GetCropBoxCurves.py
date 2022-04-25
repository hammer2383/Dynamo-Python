import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import clr

clr.AddReference("RevitNodes")
import Revit

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

#The inputs to this node will be stored as a list in the IN variables.
if isinstance(IN[0], list):
	view = UnwrapElement(IN[0])
	toggle = 0
else:
	view = [UnwrapElement(IN[0])]
	toggle = 1
	
listout = []

for x in view:
	if x.CropBoxActive == False:
		TransactionManager.Instance.EnsureInTransaction(doc)
		x.CropBoxActive = True
		x.CropBoxVisible = False		
		TransactionManager.Instance.TransactionTaskDone()
	region = x.GetCropRegionShapeManager().GetCropShape()
	if len(region) > 0:
		lines = [y.ToProtoType() for y in region[0]]
		listout.append(lines)
	else:
		listout.append([])



#Assign your output to the OUT variable.
if toggle == 0:
	OUT = listout
else:
	OUT = lines