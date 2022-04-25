
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
collector = FilteredElementCollector(doc)
StFrame = collector.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()


def ChangeFramingParam(framing):    	
	ZOffset = BuiltInParameter.Z_OFFSET_VALUE
	StartOffset = BuiltInParameter.STRUCTURAL_BEAM_END0_ELEVATION
	EndOffset = BuiltInParameter.STRUCTURAL_BEAM_END1_ELEVATION 
	
	ZOffsetValue = framing.get_Parameter(ZOffset).AsDouble()	
 
	StartParam = framing.get_Parameter(StartOffset)
	EndParam = framing.get_Parameter(EndOffset) 
	StartValue = StartParam.AsDouble()
	EndValue = EndParam.AsDouble()
 
	def ChangeValue():
		"""Chnage 2 values to a ZOffsetValue and set ZOffset to 0.00 after thant. 

		Returns:
			Revit Beam: Revit structural framing.
		"""	
		TransactionManager.Instance.EnsureInTransaction(doc)
		framing.get_Parameter(StartOffset).Set(ZOffsetValue)
		framing.get_Parameter(EndOffset).Set(ZOffsetValue)			
		framing.get_Parameter(ZOffset).Set(0.00)			
		TransactionManager.Instance.TransactionTaskDone()
		return framing
 
	if StartValue != 0.0 or EndValue != 0.0:
		pass
	
	else:
		if ZOffsetValue == 0.0: 
			pass
		else:
			return ChangeValue()


log1 = [] #to see out put
for f in StFrame:
    try:
    	if f.Symbol.Family.IsInPlace or doc.GetElement(f.GroupId) is not None or not hasattr(f.get_Parameter(BuiltInParameter.Z_OFFSET_VALUE), "AsDouble"):
        	continue
    except AttributeError:
        assert False, f.Id
    else:
    	log1.append(ChangeFramingParam(f))
     
OUT = log1