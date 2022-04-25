# Enable Python support and load DesignScript library
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

cuttingelem = UnwrapElement(IN[0]) #Main Element
cutelem = UnwrapElement(IN[1]) #Cutting Elements

ConType = UnwrapElement(IN[2]) # Type of connection select from project
ConType =ConType.GetTypeId()	

TransactionManager.Instance.EnsureInTransaction(doc)

for i in cutelem:
	elems = [cuttingelem.Id, i.Id]
	elemIds = List[ElementId](elems)
	Structure.StructuralConnectionHandler.Create(doc, elemIds, ConType)
	
TransactionManager.Instance.TransactionTaskDone()

OUT = "Yay!"