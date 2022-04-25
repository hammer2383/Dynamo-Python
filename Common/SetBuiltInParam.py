import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Element, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
oneView = UnwrapElement(IN[0][0])
VN = BuiltInParameter.VIEW_NAME


TransactionManager.Instance.EnsureInTransaction(doc)
OUT = oneView.get_Parameter(VN)
TransactionManager.Instance.TransactionTaskDone()

