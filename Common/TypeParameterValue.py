import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Element
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

def TypeParameterValuebyName(element, paramname):
	ETypeID = element.GetTypeId()
	EType = doc.GetElement(ETypeID)
	Eparam = EType.GetParameters(str(paramname))
	Eparam = Eparam[0]
	return Eparam.AsString()