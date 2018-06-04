from time import sleep
from os import system
from math import floor
from sys import exit

class Grid:
    def __init__(self):
        self.grid = [[[[1,2,3,4,5,6,7,8,9], False] for i in range(0,9)] for j in range(0,9)]

    def DrawGrid(self):
        print(' _______________________ ')
        print('|       |       |       |')
        for row in range(0,9):
            tmp = '| '
            for col in range(0,9):
                if len(self.grid[row][col][0]) == 1:
                    tmp += (str(self.grid[row][col][0][0]) + ' ')
                else:
                    tmp += '  '
                if col == 2 or col == 5:
                    tmp += '| '
            tmp += '|'
            print(tmp)
            if row == 2 or row == 5:
                print('|_______|_______|_______|')
                print('|       |       |       |')
        print('|_______|_______|_______|')

    def InitializeGrid(self,path):
        f = open(path)
        r = 0
        for l in f.readlines():
            vals = l.rstrip().split(',')
            for c in range(0,9):
                if int(vals[c]) != 0:
                    self.grid[r][c][0] = [int(vals[c])]
            r += 1
        f.close()

    def RemoveValueFromCell(self,value,row,col):
        if value in self.grid[row][col][0] and len(self.grid[row][col][0]) > 1:
            self.grid[row][col][0].remove(value)

    def RemoveValueFromRow(self,value,row):
        for col in range(0,9):
            self.RemoveValueFromCell(value,row,col)

    def RemoveValueFromColumn(self,value,col):
        for row in range(0,9):
            self.RemoveValueFromCell(value,row,col)

    def RemoveValueFromGroup(self,value,row,col):
        y = 3 * floor(row/3)
        x = 3 * floor(col/3)
        rows = [i for i in range(y,y+3)]
        cols = [j for j in range(x,x+3)]
        for r in rows:
            for c in cols:
                self.RemoveValueFromCell(value,r,c)

    # this function probably isn't necessary
    def ResetCheckFlags(self):
        for row in self.grid:
            for col in row:
                col[1] = False

    def SimpleScanSinglePass(self):
        foundmatch = False
        for row in range(0,9):
            for col in range(0,9):
                if len(self.grid[row][col][0]) == 1 and not self.grid[row][col][1]:
                    foundmatch = True
                    value = self.grid[row][col][0][0]
                    self.RemoveValueFromColumn(value,col)
                    self.RemoveValueFromRow(value,row)
                    self.RemoveValueFromGroup(value,row,col)
                    self.grid[row][col][1] = True
        return foundmatch

    def FindOnlyValueInRow(self):
        foundmatch = False
        for row in self.grid:
            missingValues = []
            seenValues = []
            for col in row:
                if not col[1]:
                    for val in col[0]:
                        if val not in missingValues:
                            missingValues.append(val)
            for col in row:
                if not col[1]:
                    for val in col[0]:
                        if val not in seenValues:
                            seenValues.append(val)
                        else:
                            if val in missingValues:
                                missingValues.remove(val)
            if len(missingValues) > 0:
                foundmatch = True
                for val in missingValues:
                    for col in row:
                        if val in col[0]:
                            col[0] = [val]
        return foundmatch

    def FindOnlyValueInColumn(self):
        foundmatch = False
        for x in range(0,9):
            missingValues = []
            seenValues = []
            for y in range(0,9):
                if not self.grid[y][x][1]:
                    for val in self.grid[y][x][0]:
                        if val not in missingValues:
                            missingValues.append(val)
            for y in range(0,9):
                if not self.grid[y][x][1]:
                    for val in self.grid[y][x][0]:
                        if val not in seenValues:
                            seenValues.append(val)
                        else:
                            if val in missingValues:
                                missingValues.remove(val)
            if len(missingValues) > 0:
                foundmatch = True
                for val in missingValues:
                    for y in range(0,9):
                        if val in self.grid[y][x][0]:
                            self.grid[y][x][0] = [val]
        return foundmatch

    def CheckIfSolved(self):
        # check if each cell has been checked
        for row in self.grid:
            for col in row:
                if not col[1]:
                    return False
        # check rows
        for row in self.grid:
            vals = []
            for col in row:
                if len(col[0]) != 1:
                    return False
                vals.append(col[0][0])
            # check for duplicate values
            for i in range(0,9):
                if vals[i] in vals[i+1:]:
                    return False
        # check columns
        for col in range(0,9):
            vals = []
            for row in range(0,9):
                vals.append(self.grid[row][col][0][0])
            # check for duplicate values
            for i in range(0,9):
                if vals[i] in vals[i+1:]:
                    return False
        # check 3x3 grids
        for y in range(0,7,3):
            rows = [i for i in range(y,y+3)]
            for x in range(0,7,3):
                vals = []
                cols = [i for i in range(x,x+3)]
                for row in rows:
                    for col in cols:
                        vals.append(self.grid[row][col][0][0])
                # check for duplicate values
                for i in range(0,9):
                    if vals[i] in vals[i+1:]:
                        return False
        return True

#debug
# set up window
system('cls')
s = Grid()
s.InitializeGrid('sudoku.txt')
print('Initial grid:')
s.DrawGrid()
sleep(1)

# use the simple scanning algorithm first
while s.SimpleScanSinglePass():
    system('cls')
    print('Filling in squares...')
    s.DrawGrid()
    sleep(1)

# are we done?
if s.CheckIfSolved():
    print('\n\nSOLVED')
    exit()

keepgoing = True
while keepgoing: 
    keepgoing = False
    if s.FindOnlyValueInRow():
        keepgoing = s.SimpleScanSinglePass()
        system('cls')
        print('Filling in squares...')
        s.DrawGrid()
        sleep(1)
    if s.FindOnlyValueInColumn():
        keepgoing = s.SimpleScanSinglePass()
        system('cls')
        print('Filling in squares...') # remove...
        s.DrawGrid()
        sleep(1)

# use the scanning algorithm again
while s.SimpleScanSinglePass():
    system('cls')
    print('Filling in squares...')
    s.DrawGrid()
    sleep(1)
system('cls')
print('Filling in squares...')
s.DrawGrid()

# are we done?
if s.CheckIfSolved():
    print('\n\nSOLVED')
    exit()

print('\n\nI give up')