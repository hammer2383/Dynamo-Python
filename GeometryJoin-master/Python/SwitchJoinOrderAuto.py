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

# Just for showing the category and surrender category
mappingDictionary = {
"Walls" : ("Floors", "Structural Columns"),
"Floors" : ("Structural Framing"),
"Structural Framing" : ("None"),
"Structural Columns" : ("Structural Framing", "Floors", "Structural Foundations"),
"Structural Foundations" : ("Floors", "Walls")

}

def createMultiCategoryFilter():
    """Create multi category filter instace to use in getAllModelElement

    Returns:
        obj: filter instace
    """
    listOfCategories = list()
    listOfCategories.append(db.BuiltInCategory.OST_Floors)
    listOfCategories.append(db.BuiltInCategory.OST_StructuralColumns)
    listOfCategories.append(db.BuiltInCategory.OST_StructuralFraming)
    listOfCategories.append(db.BuiltInCategory.OST_StructuralFoundation)
    listOfCategories.append(db.BuiltInCategory.OST_Walls)
    iCollectionOfCategoriesForMultiCategoryFIlter = List[db.BuiltInCategory](listOfCategories)
    multiCategoryFilter = db.ElementMulticategoryFilter(iCollectionOfCategoriesForMultiCategoryFIlter)
    return multiCategoryFilter

def getAllModelElements(doc):
    """get all model using filter from createMultiCategoryFilter

    Args:
        doc (object): Revit document

    Returns:
        list: list of elements from filter
    """
    multiCategoryFilter = createMultiCategoryFilter()
    allIdsOfModelElements = db.FilteredElementCollector(doc).WherePasses(multiCategoryFilter).WhereElementIsNotElementType().ToElementIds()
    allElementsOfModel = map(lambda x: doc.GetElement(x), allIdsOfModelElements)
    return allElementsOfModel

# Mape piszemy w schemacie: elementy jakiej kategori mają być nadrzędne nad jakimi kategoriami
def createMappingDictionary():
    mapType = {
    "Walls" : ("Floors", "Structural Columns"),
    "Floors" : ("Strcutral Framing", "Structural Columns"),
    "Structural Framing" : ("None"),
    "Structural Columns" : ("Structural Framing", "Floors", "Structural Foundations"),
    "Structural Foundations" : ("Floors", "Walls")
    }
    return mapType

def properSwitchOfElements(revitElement, joinedElement, surrenderElementTypes, doc):
    """Switch joining order of 2 elements

    Args:
        revitElement (obj): Primary Revit element
        joinedElement (obj): secondary Revit element
        surrenderElementTypes (tuple): tuple of string representation of surrender category(cutting category of Primary element)
        doc (obj): Revit document
    """
    joinedElementCategoryName = joinedElement.Category.Name
    if joinedElementCategoryName in surrenderElementTypes:
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
    """ultilising previous function to manage joined elements.

    it'll check with every joined elements to see if joining order is correct.
    Using properSwitchOfElements function.

    surrenderElementTypes is a tuple of type that would be cutting type of revitElement     

    Args:
        revitElement (obj): Revit element
        doc (obj): Revit document
    """
    joinedElementIds = db.JoinGeometryUtils.GetJoinedElements(doc, revitElement)
    mappingDictionary = createMappingDictionary()
    revitElementCategoryName = revitElement.Category.Name
    surrenderElementTypes = mappingDictionary[revitElementCategoryName]
    for joinedId in joinedElementIds:
        joinedElement = doc.GetElement(joinedId)        
        properSwitchOfElements(revitElement, joinedElement, surrenderElementTypes, doc)
        

def main():
    """run all function

    Returns:
        obj: List of Revit elements
    """
    doc = DocumentManager.Instance.CurrentDBDocument
    allModelElements = getAllModelElements(doc)
    lst = list()
    TransactionManager.Instance.EnsureInTransaction(doc)
    for revitElement in allModelElements:
        lst.append(manageJoinedElements(revitElement, doc))
    TransactionManager.Instance.TransactionTaskDone()
    return allModelElements
OUT = main()
