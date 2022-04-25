import clr
import RevitServices
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import SketchEditScope
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
floor = UnwrapElement(IN[0])
floorskId = floor.SketchId
"""TEST"""
SES = SketchEditScope(doc,"testSES")
# SES.Start()
# 
# SES.Commit()
fskd = doc.GetElement(floorskId)

OUT = fskd.GetAllElements()