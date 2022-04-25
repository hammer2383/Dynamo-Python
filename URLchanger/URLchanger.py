
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
"""
    This Scripts will Update all path of external catalogs when the project file were moved.    

"""

DOCFOLDER = "01_REVIT MODEL"
CATALOGFOLDER = "03_DOCUMENT & UTILITY"
USECORNERSTONE = False
CORNERSTONEPATH = None

doc = DocumentManager.Instance.CurrentDBDocument

if USECORNERSTONE:
    DOCDIRECTORY = path.split(CORNERSTONEPATH)[0]
else:    
    DocFilePath = doc.PathName
    DOCDIRECTORY = path.split(DocFilePath)[0]   

DOCCOMPO = list(DOCDIRECTORY.split(sep))
DOCCOMPO[0] = DOCCOMPO[0] + sep

def FindIndex(Path, TargetFolder):
    """Find the index of the target folder

    Args:
        Path (string): string of path
        TargetFolder (str): Name of the outer most folder where all catalogs reside

    Returns:
        int: Indexes of the Target Folder
    """
    PathCompo = Path
    PathCompo = list(PathCompo.split(sep))    
    PathCompo[0] = PathCompo[0] + sep
    TargetIndex = PathCompo.index(TargetFolder)
    return TargetIndex

def NewPath(Item):
    """Append catalog's path to new project path        

    Args:
        Item (Revit family): Revit family

    Returns:
        str: new abosolute path of Catalog's path
    """
    oldpath = Item.LookupParameter("Catalog").AsString()
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
                nextpath = NewPath(i)
                SetPath(i, nextpath)
                AllUpdatedpath.append(nextpath)
            except ValueError:            	
                continue
            
    return AllUpdatedpath    
    
OUT = mainDefualt()
