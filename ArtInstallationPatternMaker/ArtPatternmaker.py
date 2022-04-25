
def nextnumber(n,n1):
    #n second prev
    #n1 prev
    if n == 0:
        nextnum = 0
    elif n == 1:
        nextnum = 2
    elif n == 2:
        nextnum = 1
    return nextnum

def patternGen(stnum, nxnum, col, row):    
    #make row
    wall= [[stnum],[nxnum]]  
    for r in range(row-2):
        length = len(wall)
        nextnum = nextnumber(wall[length-2][0],wall[length-1][0])
        wall.append([nextnum])

    #mod column
    wallindex = 0            
    for w in wall:
        for c in range(col-1):
            #count = c
            if wallindex == 0 and len(w)==1:
                w.append(nxnum)
                #assert False, wallindex
            elif len(w) == 1 and wallindex != 0:
                if col < 3:
                    if wall[wallindex-1][c] == 1:
                        newnum = 2
                    elif wall[wallindex-1][c] == 2:
                        newnum = 1
                    elif wall[wallindex-1][c] == 0:
                        newnum = 0
                    w.append(newnum)
                else:                    
                    w.append(wall[wallindex-1][c+2])            
            elif len(w)!= 0:                
                length = len(w)
                nextnum = nextnumber(w[length-2],w[length-1])
                w.append(nextnum)
        wallindex += 1

    return wall

from itertools import chain

def addstar(PatternList,inter,ele):    
    PatternList = list(chain(*[PatternList[i:i+inter] + [ele] if len(PatternList[i:i+inter]) == inter else PatternList[i:i+inter] for i in range(0, len(PatternList), inter)]))
    return PatternList


def AddGap(pattern, Cinterval, Rinterval):
    PatternList = pattern
    blank = []
    for row in PatternList:
        blank.append(addstar(row, Cinterval,'.'))
        
    PatternList = blank
    
    ele = ['.' for i in range(len(PatternList[0]))]
    PatternList = addstar(PatternList, Rinterval, ele)
    return PatternList 

                
PatternList = patternGen(1,0,int(IN[0]),int(IN[1]))   

PatternList = AddGap(PatternList, 3, 5)           

OUT = PatternList
        
    
    

            
            
            
            
    
    
        
    
