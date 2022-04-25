"""Code from https://forum.dynamobim.com/t/save-families-from-revit-to-a-path/3983/3"""

import clr
import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

import os
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk

clr.AddReference('RevitServices')

import RevitServices

from RevitServices.Persistence import DocumentManager

from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

#Close all transactions
trans = TransactionManager.Instance
trans.ForceCloseTransaction()


fams = IN[0]
paths = IN[1]
categorys = IN [2]
FamilyName = IN[3]



#unwrap the Dynamo elements

fams = map(UnwrapElement, fams)

for i in range(len(fams) ):
    try:
        famDoc = doc.EditFamily(fams[i])
    except:
        continue
    
    cat = categorys[i]
    if cat == "null":
        cat = fams[i].FamilyCategory.Name
    famNam = FamilyName[i] + ".rfa"    
    folderpath = os.path.join(paths, cat)
    try:
        os.mkdir(folderpath)
    except:
        pass
    filepath = os.path.join(folderpath, famNam)
    try:
    	famDoc.SaveAs(filepath)

    	famDoc.Close(False)
    except:
    	pass
    
OUT = 0