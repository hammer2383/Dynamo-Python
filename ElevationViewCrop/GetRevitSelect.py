# By Dimitar Venkov and Cyril Poupin
import clr
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break
		
out = []
selectElemId = uidoc.Selection.GetElementIds()
selectElem = [doc.GetElement(xId) for xId in selectElemId]

for i in selectElem:
	try:
		check = Revit.Elements.ElementWrapper.Wrap(i, True)
	except: check = None

	if check is None:
		out.append(ueWrapper.Invoke(None, (i, False)))
	else:
		out.append(i) 

OUT = out
