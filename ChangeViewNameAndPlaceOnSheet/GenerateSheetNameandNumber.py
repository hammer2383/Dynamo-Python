    """Name generator with very very specific convention

    Returns:
        Tuple: (ListOfName, ListOfnumber)
    """


LEVEL = IN[0]
SHEETNAME = IN[1]
STARTNUMBER = int(IN[2])
NUMPREFIX = IN[3]

def SheetnameANdNumber(levels,sheetname,NumberPrefix,StartingNumber):
    """Generate Sheet name and Number, based on name format inside the loop.    

    Args:
        levels (str,int): level digit(int) and mark(str) 
        sheetname (str): sheet common name
        NumberPrefix (str): Prefix of number
        StartingNumber (int): starting number

    Returns:
        tuple: List of sheet name and list of sheet number
    """
    ListOfName = list()
    ListOfNumber = list()
    
    # Name are define by level so this will loop throught each level
    i = 0
    for l in levels:
        # Name format
        newname = sheetname + " " + str(l)
        number = StartingNumber + i
        SheetNumber = NumberPrefix + "-" + str(number)
        ###
        
        ListOfName.append(newname)
        ListOfNumber.append(SheetNumber)
        
        i += 1
    
        
    return ListOfName,ListOfNumber


OUT = SheetnameANdNumber(LEVEL, SHEETNAME, NUMPREFIX, STARTNUMBER)