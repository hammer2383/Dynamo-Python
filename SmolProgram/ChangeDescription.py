import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
ActiveView = UnwrapElement(IN[1])
collector = FilteredElementCollector(doc, ActiveView.Id)
stframe = collector.OfCategory(BuiltInCategory.OST_StructuralFraming).ToElements()



def ChangeFramingDescription(framing):
	FTypeID = framing.GetTypeId()
	FType = doc.GetElement(FTypeID)
	try:
		Height = FType.GetParameters("h")[0].AsValueString()
		Width = FType.GetParameters("b")[0].AsValueString()
	except ValueError:
		Width = FType.GetParameters("d")[0].AsValueString()
		Height = FType.GetParameters("bf")[0].AsValueString()
	newDescription = Width + "x" + Height
 
	TransactionManager.Instance.EnsureInTransaction(doc)
	FType.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION).Set(newDescription)
	TransactionManager.Instance.TransactionTaskDone()
	
	

OUT = map(ChangeFramingDescription,stframe)
