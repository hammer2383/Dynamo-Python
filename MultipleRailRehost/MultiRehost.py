import clr
from System.Collections.Generic import *
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Vector

from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

ELEMENTS = UnwrapElement(IN[0])
NEWHOSTS = UnwrapElement(IN[1])
VECTOR = UnwrapElement(IN[2].AsPoint()).ToXyz()

# This function
def CopyAndPlace(items, xyz = VECTOR, rehost=False):
    '''Copy and place it in by location(relative)'''
    ids = list()
    for item in items:
        ids.append(item.Id)	
    itemlist = List[ElementId](ids)

    TransactionManager.Instance.EnsureInTransaction(doc)
    if rehost:
        newitems = ElementTransformUtils.CopyElements(doc,itemlist,doc,Transform.CreateTranslation(xyz),None)
    else:
        newitems = ElementTransformUtils.CopyElements(doc,itemlist,xyz)
    TransactionManager.Instance.TransactionTaskDone()

    elementlist = list()
    for item in newitems:
        elementlist.append(doc.GetElement(item).ToDSType(False))

    return UnwrapElement(elementlist)

def ReHost(element, newhost):
    TransactionManager.Instance.EnsureInTransaction(doc)
    hostId = newhost.Id
    element.HostId = hostId
    TransactionManager.Instance.TransactionTaskDone()

def Main():
	try:
		for host in NEWHOSTS:
		    newelements = CopyAndPlace(ELEMENTS)
		    # assert False, UnwrapElement(newelements)			    
		    for e in newelements:
		        ReHost(e, host)
		return "Succes"
	except:
		return "Failed"
	
OUT = Main()
CopyAndPlace()