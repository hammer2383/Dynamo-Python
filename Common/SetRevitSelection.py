# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
import System

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

eleId=[]

for i in UnwrapElement(IN[0]):
	eleId.append(i.Id)
	
elemIds = List[ElementId](eleId)

try:
	uidoc.Selection.SetElementIds(elemIds)
	OUT = IN[0]
except:
	OUT = "Failed to set selection"