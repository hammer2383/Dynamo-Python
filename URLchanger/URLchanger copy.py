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

from os import path, sep

#######################################

DOCFOLDER = "01_REVIT MODEL"
CATALOGFOLDER = "03_DOCUMENT & UTILITY"
USECORNERSTONE = IN[1]
CORNERSTONEPATH = IN[2]

doc = DocumentManager.Instance.CurrentDBDocument

if USECORNERSTONE:
    DOCDIRECTORY = path.split(CORNERSTONEPATH)[0]
else:    
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

def NewPath(Item):
    oldpath = path.abspath(Item.LookupParameter("Catalog").AsString())
    oldpathCompo = list(oldpath.split(sep))
    # assert False, oldpath
    TargetIndex = FindIndex(DOCDIRECTORY, DOCFOLDER)
    TargetIndex2 = FindIndex(oldpath, CATALOGFOLDER)
    internalpathCompo = oldpathCompo[TargetIndex2:]    
    exteriorCompo = DOCCOMPO[:TargetIndex]    
    NewCompo = exteriorCompo + internalpathCompo
    
    return path.join(*NewCompo)

def SetPath(Item, newpath):
    TransactionManager.Instance.EnsureInTransaction(doc)
    Item.LookupParameter("Catalog").Set(newpath)
    TransactionManager.Instance.TransactionTaskDone()
    
def UpdateThePath(item):
    UpdatedPath = NewPath(item)
    SetPath(item, UpdatedPath)
    return UpdatedPath


allType = FilteredElementCollector(doc).WhereElementIsElementType().ToElements()
allTypeWtCatalog = [x for x in allType if x.LookupParameter("Catalog") is not None]


def mainDefualt():
    AllUpdatedpath = list()
    for i in allTypeWtCatalog:
        checkpath = i.LookupParameter("Catalog").AsString()
        if checkpath is None or checkpath == '':
            continue
        else:
            try:
                updated = UpdateThePath(i)
                AllUpdatedpath.append(updated)
            except ValueError:
                continue
            
    return AllUpdatedpath    
    
OUT = NewPath(allTypeWtCatalog)
