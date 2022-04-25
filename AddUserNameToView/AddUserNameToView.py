PPNElementsList = IN[0]
Views = UnwrapElement(IN[1])
FolderName = IN[2]
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FamilyManager

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
ViewList = PPNElementsList(Views)
ViewList.FilterOutbyParamValue("Folder", FolderName)

def AddingPrefix(Prefix,ViewName):
	"""Return False if they is already a Prefix"""
	#Check if view Already have Prefix
	newname = ''
	if Prefix.lower() in ViewName.lower():
	    return False	 
	else:
	    newname = Prefix + "_" + ViewName
	    return newname
	    
doc = DocumentManager.Instance.CurrentDBDocument
Flist = []
TransactionManager.Instance.EnsureInTransaction(doc)
for v in ViewList.getElements():
	vname = v.LookupParameter("View Name").AsString()
	if AddingPrefix is False:
		continue
	else:
		ap = AddingPrefix(FolderName, vname)
		doc.Set(v.LookupParameter("View Name"), ap)
		Flist.append(ap)
TransactionManager.Instance.TransactionTaskDone()
OUT = Flist