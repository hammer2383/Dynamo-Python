import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Element

E1 = UnwrapElement(IN[0])

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