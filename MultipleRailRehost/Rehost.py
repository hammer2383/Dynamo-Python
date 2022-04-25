import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

doc = DocumentManager.Instance.CurrentDBDocument

railing = UnwrapElement(IN[0])
newhost = UnwrapElement(IN[1])

TransactionManager.Instance.EnsureInTransaction(doc)

hostId = newhost.Id
railing.HostId = hostId

TransactionManager.Instance.TransactionTaskDone()

OUT = railing