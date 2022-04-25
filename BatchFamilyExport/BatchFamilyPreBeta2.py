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

# All input were
fams = IN[0]
paths = IN[4][0] # list of family
isRun = IN[1] # Folder path.
categorys = IN[2] # list of string of representation of categories
FamilyName = IN[3] # Name of the family(str)
SelectedCat = IN[4][1] # str

#unwrap the Dynamo elements
fams = map(UnwrapElement, fams)
if not isRun:
	raise ValueError
for i in range(len(fams)):   
    
    cat = categorys[i]
    # string together a family name
    if cat not in SelectedCat:    	
    	continue
    try:
        # it will throw an error if the family is non-loadble
        famDoc = doc.EditFamily(fams[i])
    except:
        raise TypeError
    
    famNam = FamilyName[i] + ".rfa"
    # folder path to be create    
    folderpath = os.path.join(paths, cat)    
    #Create folder
    try:
        os.mkdir(folderpath)
    except OSError:
        pass
    filepath = os.path.join(folderpath, famNam)
    
    # Save the family, some family would pop up some error and can't be save.
    # which would be safely ignore.    
    try:
    	famDoc.SaveAs(filepath)
    	famDoc.Close(False)
    except:
    	pass
    
OUT = 0
