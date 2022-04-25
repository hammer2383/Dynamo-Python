"""These code will generate Art Installation pattern.
this is one of the pattern
        [[0,1,0,2,0],
         [4,0,3,0,4],
         [0,2,0,3,0]]
"""


from itertools import chain


def HNextNumber(n):
    """Determine the next number based on the preultimate number in horizontal direction(left to right).

    the function check which pair the number belonged to and return on of its pair.

    Args:
        n (int): preultimate number

    Returns:
        int: next number according to local norseq
    """
    # normal pairs (horizontal direction)
    norseq = ((1, 2),
              (3, 4))
    nextnum = 0

    if n == 0:
        nextnum = 0
    else:
        for s in norseq:
            if n in s:
                tseq = list(s[:])
                tseq.remove(n)
                nextnum = tseq[0]

    return nextnum


def VNextNumber(topright):
    """Determine the next number based on the preultimate number in diagonal direction(buttom left to right).

    the function check which pair number belonged to and return on of its pair.
    The topright agrument is usually top right from the previous number (hence the name)
    [1,3,1]
    [4,5,4] top right of 4 will be 3 in graphical sense.

    Args:
        n (int): preultimate number

    Returns:
        int: next number according to local norseq
    """

    nextnum = 0
    # dianogal pairs
    seq = ((1, 4),
           (2, 3))

    if topright == 0:
        nextnum = 0
    else:
        for s in seq:
            if topright in s:
                tseq = list(s[:])
                tseq.remove(topright)
                nextnum = tseq[0]
    return nextnum


def patternGen(stnum, nxnum, col, row):
    """Generate whole with specific column and row.

    Whole pattern generate by VNextNumber and HNextNumber function using its local variable
    "seq" and "norseq"(in mentioning order)
    it will create all the specific row first then add elements in each row later.

    Args:
        stnum (int): number of the first row
        nxnum (int): fist number of the second row
        col (int): number of desired column
        row (int): number of desired row

    Returns:
        list: list like array of pattern
    """

    # make row
    wall = [[stnum], [nxnum]]  # adding neccessary first 2 rows
    # addin the rest (N-2)
    for r in range(row-2):
        length = len(wall)
        nextnum = HNextNumber(wall[length-2][0])
        wall.append([nextnum])

    # add column
    RowIndex = 0
    for row in wall:
        for c in range(col-1):  # all first column were create for row, remember?
            # add second column of first row according to next row
            if RowIndex == 0 and len(row) == 1:
                row.append(VNextNumber(wall[1][0]))
                continue
            # add the rest of the fisrt row
            elif RowIndex == 0 and len(row) > 1:
                row.append(HNextNumber(row[-2]))
                continue
            # add the rest of column of each row
            elif RowIndex > 0:
                # check for last column case
                if c == col-2:
                        row.append(HNextNumber(row[-2]))
                else:
                    row.append(VNextNumber(wall[RowIndex-1][c+2]))
        RowIndex += 1

    return wall


def addstar(PatternList, inter, ele):
    """add element at specific interval in list.

    Args:
        PatternList (List): list of pattern
        inter (int): interval
        ele (str): element to add

    Returns:
        list: same list structure as PatternList with added element
    """
    # Search stack overflow for this line of code lol
    PatternList = list(chain(*[PatternList[i:i+inter] + [ele] if len(PatternList[i:i+inter])
                       == inter else PatternList[i:i+inter] for i in range(0, len(PatternList), inter)]))
    return PatternList


def AddGap(pattern, Cinterval, Rinterval):
    """inserts gap in the pattern.
    Since art wall has gap between them
    in this particular code, the gap will be hard coded to start after 5th row and 2nd column
    just like the actual wall.

    Args:
        pattern (List): list of pattern
        Cinterval (int): number of column before gap
        Rinterval (int): number of row before gap

    Returns:
        list: same list structure as pattern with added gap
    """
    PatternList = pattern  # just aliasing
    Gapped = []
    # Start adding gap after 2nd column
    for row in PatternList:
        Columnoffset = row[0:1] + ['.']  # add a '.' after 2nd column
        restrow = row[1:]
        restrow = addstar(restrow, Cinterval, '.')  # add the rest of dot
        addrow = Columnoffset + restrow
        Gapped.append(addrow)

    PatternList = Gapped

    # adding gap for after 5th Row
    # Creating list of '.' with same number of elements as column
    ele = ['.' for i in range(len(PatternList[0]))]
    RowOffset = PatternList[0:5] + [ele]  # add a row of '.' after 5th row
    assert True, RowOffset
    RestRow = PatternList[5:]
    RestRow = addstar(RestRow, Rinterval, ele)  # normally add gap
    PatternList = RowOffset + RestRow  # combine
    return PatternList

PatternList = patternGen(int(IN[2]), int(IN[3]), int(IN[0]), int(IN[1]))
PatternList = AddGap(PatternList, 3, 6)


def RowDistance(array,btwelem,btwset):
    """Create placing distance for each module.
    
    each distance is how far from the wall's origin point with 
    the '.' represent blank space.
    
    example:
    btwelem = 2, btwset = 3
    [1,3,1,'.',3,1,3] could translate to this [0,2,4,9,11,13]    
    in this function
    the '.' mean add gap distance to the next element distance, which defined by "btwset" argurement
    
               
    Args:
        array (list): Pattern of the wall with '.' as gap
        btwelem (float): distance between each modules origin point in vertical direction
        btwset (float): distance between each set of modules in vertical direction

    Returns:
        list: list of row's distance
    """
    DistanceList = []
    count = 0
    withgap = False # use to set next iteration behavior
    for row in array:
        prevDistance = DistanceList[-1]	
        if set(row) == {"."}:
            withgap = True
            count += 1
            continue
        elif withgap and set(row) != {"."}:         
            DistanceList.append(prevDistance-(btwelem+btwset))
            withgap = False
        else:
            if count == 0:
                DistanceList.append(0)
            else:			
                DistanceList.append(prevDistance-btwelem)
        count += 1
    return DistanceList
            
OUT = PatternList
