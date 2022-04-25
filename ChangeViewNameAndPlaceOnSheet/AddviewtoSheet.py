import clr
# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import Viewport, XYZ

VIEWS = UnwrapElement(IN[0]) # View to add to the sheets
SHEET = UnwrapElement(IN[1]) # Sheet for view to be put in
DewIt = IN[2] # Boolean, True to run

#Xcod = IN[2][0]
#Ycod = IN[2][1]
#Zcod = IN[2][2]

doc = DocumentManager.Instance.CurrentDBDocument

def CreateViewport(doc, sheet, view, location):
    """Create view port on sheet(places view on sheet).

    Args:
        doc (DocumentManager): current active document
        sheet (Revit sheet): Revit sheet
        view (Revit view): Revit view
        location (XYZ): location for viewport origin
    """
    sheetid = sheet.Id
    viewid = view.Id
    try:
        Viewport.Create(doc, sheetid, viewid, location)
    except Exception:
        False

def IsSameSurfix(sheet, view):
    """Check if sheet name and view name have the same level number.
    it's assumed;sheet and view name have level number at the end.

    Args:
        sheet (Revit sheet): Revit sheet
        view (Revit view): Revit view

    Returns:
        Boolean: Is sheet and view name is of the same level
    """
    SheetName = sheet.ViewName
    SheetSurfix = SheetName.split()
    
    ViewName = view.ViewName
    ViewSurfix = ViewName.split()
    return SheetSurfix[-1] == ViewSurfix[-1]



location = XYZ(1.4,1.64,0) # Hardcoded for now

# Adding View to Sheet
def Main(DewIt):
    SheetViewPair = [] # a pair of matching level denotion of view and sheet; [[sheet,view],[sheet2,view2]]        
    for sheet in SHEET:        
        for view in VIEWS: 
            if IsSameSurfix(sheet,view) is True:
                SheetViewPair.append([sheet,view])
                if DewIt == True:                                      
                    TransactionManager.Instance.EnsureInTransaction(doc)
                    CreateViewport(doc, sheet, view, location)
                    TransactionManager.Instance.TransactionTaskDone()
    
    return SheetViewPair                

OUT = Main(DewIt)