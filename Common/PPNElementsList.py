"""ElementList Type for generally manage Revit elements
    i.e. filter by param value, filter by multiple paramvalue of sample element
    TODO: Switch to value converting instead of read from string.
        for more accuracy
"""


import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import Element, FilteredElementCollector, StorageType
from operator import gt,lt,ge,eq,ne,le

import re

class FilterTool(object):
    """Collection of Function
    """     
    def __init__(self):
        """USESTR(bool): only use in paramvalue function. True to set function to read string value.
        """
        self.USESTR = False # dictate function paramvalue whethever to return all value as AsValueString   

    @staticmethod
    def IsParamExist(element, paramname):
        """Private
        
            check if parameter exist and raise an exception if not        
        Args:
            element(obj): a revit element
            paramname(str): parameter name
        Return:
            None if parameter exist, raise an error if not
        """
        param = element.GetParameters(paramname)
        param = [p for p in param]
        if param == []:
            raise ValueError("Parameter not exist. check parameter name")
    @staticmethod
    def ConvertToType(value, valueToConvert):
        """Private

            Convert data type to the first argument type
        Args:
            value(obj): example
            valueToConvert(obj)
        Return:
            totype(valueToConvert)
        """
        try:
            totype = type(value)
            return totype(valueToConvert)
        except TypeError:
            return valueToConvert
    
    @staticmethod
    def removeUnit(value):
        """Private
        Args:
            value(string): value to remove any character
        Return:
            String with unit(ie. cm, mm) removed
        """
        return re.sub("[^0-9\\.]", "", value)
    
    # def changeUSEID(self, bo):
    #     self.USEID = bo

    COMP = {">": gt,
            "<": lt,
            ">=": ge,
            "<=": le,
            "==": eq,
            "!=": ne,
            }

    @classmethod
    def CompareValue(cls, value1, comparision, value2):
        """Private
            Mostly use in comparing User's input value and Revit element parameter value

        Args:
            value1(obj): value to be compare
            comparision(str): string representation of an comparison operator
            value2(obj): comparing value
        Return:
            Bool: result from comparision
        """
        value2 = cls.ConvertToType(value1, value2) #Convert to the same type
        comparision = cls.COMP[comparision]
        return comparision(value1,value2)           
        
    def paramvalue(self, element, paramname):
        """Public

        Get Parameter values of an element
        using the first parameter from GetParameters method        

        Args:
            element : revit element
            paramname (str): paramter name
        Return:
            Parameter's value of that element.
            if USESTR instance attribute is True it will return all value as AsValueString
            otherwise return:
                parameter value of a given name, data type wil depend on StorageType 
                ElementId, Double, Integer, String
        """              
        

        try:
            param = element.GetParameters(paramname) #the list of founded parameter of the same name
            param = param[0] #first paarmeter            
            paramtype = param.StorageType
            if self.USESTR is True and paramtype != StorageType.String: #Check if user want to use string value
                return param.AsValueString()

            else:
                if param.AsElementId is not None and paramtype == StorageType.ElementId:            	
                    #return param.AsValueString()                
                    return param.AsElementId()
                elif param.AsDouble() is not None and paramtype == StorageType.Double: 
                    #assert False
                    return float(self.removeUnit(param.AsValueString()))
                elif param.AsInteger() is not None and paramtype == StorageType.Integer:
                    #assert False
                    return param.AsInteger()
                elif param.AsString is not None and paramtype == StorageType.String:
                    #assert False
                    return param.AsString()            
                else:
                    raise ValueError("Error in paramvalue, None value")
    
        except ValueError:
            return None
        
    
    def CompareParamValue(self, element, compareoperator,comparingelem, parameter):
        """Public
            Comparing 2 Elements parameter's value
        Args:
            element(obj): element to be compare
            compareoperator(str): comparison operator in string
            comparingelem(ob): comparing element
            parameter(str): name of a parameter
        Return:
            Bool: result of comparison
        """
        try:            
            elemvalue = self.paramvalue(element, parameter)
            comparevalue = self.paramvalue(comparingelem, parameter)
            comp = self.COMP[compareoperator]
            return comp(elemvalue, comparevalue)
        except ValueError:
            return False

    def FilterbyParamValue(self, elements, parameter, value, reverse=False):
        """Public
            
            Filter elments by parameter name and value
            
            Args:
                elements: list of elements to be filter
                parameter: parameter names, multiple param name seperates by "|"
                reverse(bool): if True, return elements that're not met description instead                
            Return:
                Filtered elements
        """

        filtered = []
        for element in elements:
            if self.CompareValue(self.paramvalue(element, parameter), "==", value):
                filtered.append(element)
        if reverse is True:
            def Diff(li1, li2):
                return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1)))) # List Different
            reverselist = Diff(elements, filtered)
            return reverselist      

        return filtered

    def MatchMultipleParam(self, SampleElement, elements, paramset):
        """Public Get element with match parameter value of a sampling.    

        paramset contain one or more each seperated by |
        i.e. "param1|param2|param3"

        Args:
            SampleElement (Element): Revit sample element
            elements (Element): list of elements to be match
            paramset (str): parameters name, could be more than one with | as seperator

        Returns:
            Element: Revit elements that match the parameters's value.
        """
        
        paramset = paramset.split("|")
        for p in paramset:
            FilterTool.IsParamExist(SampleElement, p)
        # work by remove non match element    
        to_match = [i for i in elements] # to iterate
        matched = to_match[:] # to return
        for instance in to_match:            
            for p in paramset:
                exampvalue = self.paramvalue(SampleElement, p)
                value = self.paramvalue(instance, p)
                if exampvalue == value:
                    continue
                else:                    			
                    matched.remove(instance)
                    break
        return matched
        #out put    
        

    @classmethod
    def MatchType(cls, SampleElement, elements):
        """Public

            Filter out element that's not the same type

            Args:
                SampleElement: single sample element
                elements: Element ot be match
            Return:
                List of matched elements
        """
        matched = list()
        for element in elements:
            if SampleElement.GetTypeId() == element.GetTypeId():
                matched.append(element)
        return matched


    def MatchFamily(self, SampleElement, elements):
        """Public

            Filter out element that's not the same Family
            
            Remark:
                if custom family has the same name as system family i.e. basic wall.rfa
                it will be include it output

            Args:
                SampleElement: single sample element
                elements: Element ot be match
            Return:
                List of matched elements
        """
        matched = list()
        for element in elements:
            if self.CompareParamValue(SampleElement, "==", element, "Family"):
                matched.append(element)
        
        return matched

    
    
    def FilterbyCondition(self,elements, parameter, comparison, value):
        """Public

            Filter out element by parameter value wiht condition

            Args:
                elements(object): list of elements
                parameter(str): name of a parameter
                comparison(str): comparision
                value(str): value of parameter to be compare

            Return:
                List of filtered elements
        """        
        filtered = list()
        try:         
            for elem in elements:
                elem_value = self.paramvalue(elem, parameter)

                if self.CompareValue(elem_value,comparison, value) is True:
                    filtered.append(elem)
            return filtered
        except ValueError:
            raise ValueError("in FilterbyCondition: Wrong input Value")




#in case of name change
FilterTool = FilterTool


class PPNElementsList(FilterTool):
    """Store Revit element with filter tool inherited from FilterTool"""

    def __init__(self, elements=None, IsAllElement=False, doc=None):
        """default would be blank
        Collection of element        
        Args:
            elements(obj): List of Revit elements 1 level list only, no nested list
            IsAllElement(bool, optional): if True, It will take all of Revit element in document instead of specify one
            doc(obj, optional): Revit document, only need when IsAllElement is True
        """
        FilterTool.__init__(self)   
        if IsAllElement is True and doc is not None:
            self.doc = doc
            elements = FilteredElementCollector(doc).WhereElementIsNotElementType()
        self.elements = elements 

    def UseStringValue(self, usestr):
        """Public
            Change whethever to use actual parameter value or value as string when filter element.
            should be call agian and set to False, after done a operation

        Args:
            usestr(bool): true to use string value
        Return:
            current instance
        """
        self.USESTR = usestr
        return self    

    def getElements(self):
        """Public
            Get all Element in an instance.
        """
        elemlist = [e for e in self.elements]
        return elemlist
    
    def SetElement(self, elements):
        """Public Set new elements.

        Args:
            elements (list:Element): List of revit element

        Returns:
            List: list of new elements
        """
        self.elements = elements

    def AppendElement(self, elements):
        """Public add new list of elements. 

        Args:
            elements (list:Element): List of Revit elements

        Returns:
            self
        """
        newelement = self.getElements + elements
        self.SetElement(newelement)
        return self
        

    def ElementsInView(self, view = None):
        """later"""
        fic = []
        fec = FilteredElementCollector(self.doc, self.doc.ActiveView.Id).ToElements()
        for i in fec:
            try:
                fic.append(i.ToDSType(True))
            except:
                pass
        return fec   
    
    def MatchbyMultipleParam(self, SampleElement, paramset):
        """Public
            
            Filter out element that's not match the sample's parameter value from the instance.
            
                Args:
                    SampleElement: single sample element
                    paramset(str): parameter names, each parameter seperated by "|"
                Return:
                    self
        """

        filtered = self.MatchMultipleParam(SampleElement,self.elements, paramset)
        self.SetElement(filtered)
        return self

    def FilterOutbyParamValue(self, parameter, value, reverse=False):
        """Public
        
            Filter out element that not match a specific parameter's value from instance.
            
                Args:
                    parameter(str): a Parameter name
                    value(str): paramter's value
                Return:
                    self
        """

        filtered = self.FilterbyParamValue(self.elements, parameter, value, reverse)
        self.SetElement(filtered)
        return self
    
    def FilterOutbyParamCondition(self, parameter, condition="==", value="None"):
        """Public
            
            Filter out element with parameter by specific condition from instance.

                Args:
                    parameter(str): parameter names
                    condition
                Return:
                    self
        """
        if value == "None":
            return "Enter the value!!!"
        
        FilteredElem = self.FilterbyCondition(self.getElements(), parameter, condition, value)
        self.SetElement(FilteredElem)
        
        return self     


    def MatchbyTypeAndMultipleParam(self, SampleElement, paramset):
        """Public
        
            Get Elements with the same type and specific parameter that are the same as Sampling Element
            to instance.
            
            Args:
                SampleElement: single sample element
                paramset: parameter names, each parameter seperated by "|"
            Return:
                self
        """

        matchedtype = FilterTool.MatchType(SampleElement, self.getElements()) #element of the same type       
        match_param = self.MatchMultipleParam(SampleElement, matchedtype, paramset)
        self.SetElement(match_param)        
        return self

    def MatchType(self, SampleElement):
        """Public
            Get element of the same type as SampleElement to the instance.

            Args:
                SampleElement: single sample elemente
            Return:
                list of matched Revit elements
        """
        matchedtype = FilterTool.MatchType(SampleElement, self.getElements())
        if matchedtype == None:
            raise ValueError("None were found")
        else:            
            return matchedtype

    def MatchFamily(self, sampleElement):
        """Public
            Get elements of the same family as SampleElement to the instance.

            Args:
                SampleElement(): single sample element
            Return:
                list of matched Revit elements
        """
        matchedfam = super(PPNElementsList,self).MatchFamily(sampleElement, self.getElements())
        if matchedfam == None:
            raise ValueError("None were found")
        else:            
            return matchedfam
    
    def MatchCategory(self, sampleElement):
        """Public Return list of element with the same category as sampleElement.

        Args:
            sampleElement (Element): sample revit element

        Returns:
            list: list of matched Revit elements
        """
        matchElem = list()
        sampleCat = sampleElement.Category.Name        
        for elem in self.getElements():
            if sampleCat == elem.Category.Name:               
                matchElem.append(elem)
            else:
                continue        
        return matchElem
            
    
    def ParameterValuesByName(self, parameter):
        """Public Return list of paramter value by name.

        Args:
            parameter (str): name of the parameter

        Returns:
            list: list of value
        """
        paramvalue = []
        for e in self.getElements():  

            value = self.paramvalue(e, parameter)
            paramvalue.append(value)  

        return paramvalue


OUT = PPNElementsList