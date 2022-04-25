import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Element, BuiltInParameter
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
VIEW = UnwrapElement(IN[0])
STARTNUM = IN[1] # in this format; EE-1234
MIDDLE = IN[2]
INDEX = int(IN[3])
VN = BuiltInParameter.VIEW_NAME
PVL = BuiltInParameter.PLAN_VIEW_LEVEL


def GenerateNewName(view, prefix, middle, index: int):
    """Generate new name based on specific input and associate level.
    
    
    Args:
        view (Revit view): Revit view
        prefix (str): name prefix
        middle (str): middle name
        index (int): level denotaion of level's name

    Returns:
        str: new name
    """
    viewname = view.get_Parameter(PVL).AsString()
    SepName = viewname.split()
    NewName = prefix + " " + middle + " " + SepName[index]
    return NewName


NewViewsName = list()
TransactionManager.Instance.EnsureInTransaction(doc)

i = 0
for v in VIEW:
    sepNum = STARTNUM.split("-")
    Digit = int(sepNum[1]) + i
    ViewPrefix = sepNum[0] + "-" + str(Digit)
    
    NewName = GenerateNewName(v,ViewPrefix,MIDDLE,INDEX)
    # Change view name
    ViewNameParam = v.get_Parameter(VN).Set(NewName)        
    NewViewsName.append(NewName) # just for out put
    i += 1
OUT = NewViewsName
TransactionManager.Instance.TransactionTaskDone()