from ChangeViewNameAndPlaceOnSheet.ChangeViewName import NewName
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Element, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
SHEETS = UnwrapElement(IN[0])
SN = BuiltInParameter.SHEET_NAME

"""Highly hard coded!!!"""


def RegenName(sheet):    
    sheetname = sheet.get_Parameter(SN).AsString()
    SepName = sheet.split()
    SepName[0] = "แปลนระบบแจ้งเหตุเพลิงไหม้"
    NewName = " ".join(SepName)
    return NewName


for sheet in SHEETS:
    NewName = RegenName(sheet)
    TransactionManager.Instance.EnsureInTransaction(doc)        
    sheet.get_Parameter(SN).Set(NewName)
    TransactionManager.Instance.TransactionTaskDone()