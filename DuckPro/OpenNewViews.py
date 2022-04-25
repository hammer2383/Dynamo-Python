import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIDocument

TransactionManager.Instance.EnsureInTransaction(doc)
TransactionManager.Instance.ForceCloseTransaction()

view = UnwrapElement(IN[0])
uidoc.RequestViewChange( view )