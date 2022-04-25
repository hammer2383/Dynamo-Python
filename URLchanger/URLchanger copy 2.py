# this code is full of a bad code, a lot of bad code actually, please don't try to find and murder me, thank you :)
##############Import module##################
import clr
import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")
clr.AddReference("RevitServices")
import RevitServices
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, Element

from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from os import listdir, path, sep
from os.path import isfile, join
#######################################

DOCFOLDER = "01_REVIT MODEL"
CATALOGFOLDER = "03_DOCUMENT & UTILITY"
CORNCERSTONEID = "bea19db04fe61294adc9f1a4ee19556007c4e44a656b8745c79022b416e816d4"


doc = DocumentManager.Instance.CurrentDBDocument
DocFilePath = doc.PathName
DOCDIRECTORY = path.split(DocFilePath)[0]
DOCCOMPO = list(DOCDIRECTORY.split(sep))
DOCCOMPO[0] = DOCCOMPO[0] + sep

def FindIndex(Path, TargetFolder):
    PathCompo = path.abspath(Path)
    PathCompo = list(PathCompo.split(sep))    
    PathCompo[0] = PathCompo[0] + sep
    TargetIndex = PathCompo.index(TargetFolder)
    return TargetIndex

def SetNewPath(Item):
    oldpath = path.abspath(Item.LookupParameter("Catalog").AsString())
    oldpathCompo = list(oldpath.split(sep))
    # assert False, oldpath
    TargetIndex = FindIndex(DOCDIRECTORY, DOCFOLDER)
    TargetIndex2 = FindIndex(oldpath, CATALOGFOLDER)
    internalpathCompo = oldpathCompo[TargetIndex2:]    
    exteriorCompo = DOCCOMPO[:TargetIndex]    
    NewCompo = exteriorCompo + internalpathCompo
    
    nextpath = path.join(*NewCompo)
    Item.LookupParameter("Catalog").Set(nextpath)
    
    return nextpath

allType = FilteredElementCollector(doc).WhereElementIsElementType().ToElements()
allTypeWtCatalog = [x for x in allType if x.LookupParameter("Catalog") is not None]

AllUpdatedpath = list()
TransactionManager.Instance.EnsureInTransaction(doc)
for i in allTypeWtCatalog:
    checkpath = i.LookupParameter("Catalog").AsString()
    if checkpath is None or checkpath == '':
        continue
    else:
        try:
            updated = SetNewPath(i)
            AllUpdatedpath.append(updated)
        except ValueError:
            continue
        
TransactionManager.Instance.TransactionTaskDone()

OUT = AllUpdatedpath
