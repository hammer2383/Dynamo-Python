import clr
import System
import operator
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
import Autodesk.Revit.DB as db

# Create Revit Filter
def createMultiCategoryFilter():
    listOfCategories = list()
    listOfCategories.append(db.BuiltInCategory.OST_Floors)
    listOfCategories.append(db.BuiltInCategory.OST_StructuralColumns)
    listOfCategories.append(db.BuiltInCategory.OST_StructuralFraming)
    listOfCategories.append(db.BuiltInCategory.OST_StructuralFoundation)
    listOfCategories.append(db.BuiltInCategory.OST_Walls)
    iCollectionOfCategoriesForMultiCategoryFIlter = List[db.BuiltInCategory](listOfCategories)
    multiCategoryFilter = db.ElementMulticategoryFilter(iCollectionOfCategoriesForMultiCategoryFIlter)
    return multiCategoryFilter

# Get all elements model filterd from multiCategoryFilter
def getAllModelElements(doc):
    multiCategoryFilter = createMultiCategoryFilter()
    allIdsOfModelElements = db.FilteredElementCollector(doc).WherePasses(multiCategoryFilter).WhereElementIsNotElementType().ToElementIds()
    allElementsOfModel = map(lambda x: doc.GetElement(x), allIdsOfModelElements)
    return allElementsOfModel

def createMappingDictionary():
    mapType = {
    "Walls" : ("Floors", "Structural Columns"),
    "Floors" : ("Strcutral Framing", "Structural Columns"),
    "Structural Framing" : ("Walls"),
    "Structural Columns" : ("Structural Framing", "Floors", "Structural Foundations"),
    "Structural Foundations" : ("Floors", "Walls")
    }
    return mapType

# how would it know if it in correct order.
def properSwitchOfElements(revitElement, joinedElement, surrenderElementTypes, doc):
    joinedElementCategoryName = joinedElement.Category.Name
    if joinedElementCategoryName in surrenderElementTypes:
        # Determines whether the first of two joined elements is cutting the second element.        
        if db.JoinGeometryUtils.IsCuttingElementInJoin(doc, revitElement, joinedElement):
            try:
                db.JoinGeometryUtils.SwitchJoinOrder(doc, revitElement, joinedElement)
            except:
                pass
    else:
        if not db.JoinGeometryUtils.IsCuttingElementInJoin(doc, revitElement, joinedElement):
            try:
                db.JoinGeometryUtils.SwitchJoinOrder(doc, revitElement, joinedElement)
            except:
                pass


def manageJoinedElements(revitElement, doc):
    joinedElementIds = db.JoinGeometryUtils.GetJoinedElements(doc, revitElement)
    mappingDictionary = createMappingDictionary()
    revitElementCategoryName = revitElement.Category.Name
    surrenderElementTypes = mappingDictionary[revitElementCategoryName]
    for joinedId in joinedElementIds:
        joinedElement = doc.GetElement(joinedId)       
        properSwitchOfElements(revitElement, joinedElement, surrenderElementTypes, doc)
        

def main():
    doc = DocumentManager.Instance.CurrentDBDocument
    allModelElements = getAllModelElements(doc)
    lst = list()
    TransactionManager.Instance.EnsureInTransaction(doc)
    for revitElement in allModelElements:
        lst.append(manageJoinedElements(revitElement, doc))
    TransactionManager.Instance.TransactionTaskDone()
    return allModelElements
OUT = main()
