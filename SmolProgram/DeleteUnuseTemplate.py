import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import*
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
"""get template of every view then check for unuse template"""


views = FilteredElementCollector(doc).OfClass(View)
appliedtemplates = [v.ViewTemplateId for v in views]
templates = [v for v in views if v.IsTemplate == True]

toDelete = [] # the Revit template to be delete
DeleteName = [] # just for this display which templated were deleted
for t in templates:
	if t.Id not in appliedtemplates:
		DeleteName.append(t.Name)
		toDelete.append(t.Id)

TransactionManager.Instance.EnsureInTransaction(doc)
for e in toDelete:
	doc.Delete(e)
TransactionManager.Instance.TransactionTaskDone()

OUT = DeleteName