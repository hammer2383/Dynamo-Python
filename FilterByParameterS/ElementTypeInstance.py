
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

from System.Collections.Generic import List

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *
 
import System
from System.Collections.Generic import *

############################
#########CODE HERE##########
############################
#   Copy below dash
#---------------------------
def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

types = UnwrapElement(tolist(IN[0]) )
catNames = set()
for t in types:
	c1 = t.Category
	if c1 is not None:
		catNames.add(c1.Name)

catId = List[ElementId]()
allCats = doc.Settings.Categories
for cn in catNames:
	if allCats.Contains(cn):
		catId.Add(allCats[cn].Id)

type_storage = dict()
fec = FilteredElementCollector(doc).WhereElementIsNotElementType()
if catId:
	fec = fec.WherePasses(ElementMulticategoryFilter(catId) )

for e in fec:
	id1 = e.GetTypeId().IntegerValue
	if id1 in type_storage:
		type_storage[id1].append(e.ToDSType(True) )
	else:
		type_storage[id1] = [e.ToDSType(True)]

################################################
#Filter by Parameter############################
# this will use only first list of instance for now
################################################

def paramvalue(element, paramname):
    """Look for Parameter values
        the parameter used is the first parameter that match the name
        
        Parameters:
            element : revit element
            paramname (string): paramter name
        Return parameter value of a given name"""
    param = element.GetParameters(paramname)
    param = param[0]
    value = param.AsString()
    if value is None:
        value = param.AsValueString()        
    return value

# All instance of type
Allinstances = [type_storage.get(t.Id.IntegerValue, None) for t in types]
# List of Instances
Allinstances = UnwrapElement(Allinstances)

EXAMP = UnwrapElement(IN[1])
PARAM = IN[2]
PARAM = PARAM.split("|")

TO_MATCH = [i for i in Allinstances[0]]
MATCHED = TO_MATCH[:]
STATUS = True

for instance in TO_MATCH:
	try:
		for p in PARAM:
			exampvalue = paramvalue(EXAMP, p)
			value = paramvalue(instance, p)
			if exampvalue == value:
				match = True
			else:
				match = False			
				MATCHED.remove(instance)
				break
	except:
		STATUS = False
		break

if STATUS is True:
	OUT = MATCHED
else:
	OUT = "Check your parameters"

