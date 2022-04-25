import clr
import System
import operator
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
import Autodesk.Revit.DB as db

DeleteGroup = IN[0]
MainRun = IN[1]
def main(dodelete=False):
    # Get all groups
	AllGroup = db.FilteredElementCollector(doc).OfCategory(db.BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType()
	# Get all groups type
	AllGroupType = db.FilteredElementCollector(doc).OfCategory(db.BuiltInCategory.OST_IOSModelGroups).WhereElementIsElementType()
 
	TransactionManager.Instance.EnsureInTransaction(doc)		
	
	GroupsTypeID = []
	GroupsTypeName = []
	for i in AllGroupType:
		GroupsTypeID.append(i.Id)
		GroupsTypeName.append(i.LookupParameter("Type Name").AsString())
	if dodelete == True:
		for i in AllGroup:
			i.UngroupMembers()	
		for ID in GroupsTypeID:
			doc.Delete(ID)
	TransactionManager.Instance.TransactionTaskDone()
 
	return GroupsTypeName

if DeleteGroup == True and MainRun == True:
    OUT = main(True)
else:
	OUT = main(False)

	
	