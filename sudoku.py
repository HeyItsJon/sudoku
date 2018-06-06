"""This is my sudoku module

Other info goes here
"""
# create single function for each strategy
#   run all three possiblities and call check_cells within
# subgroup_exclusion
# hidden_twin
# chain

__version__ = '0.1'
__author__ = 'Jon Altenburger'

from time import sleep
from os import system
from math import floor
from sys import exit


class Grid:
    """Class docstring goes here
    """
    def __init__(self):
        """Docstring goes here
        """
        self.grid = [
                [
                [[1,2,3,4,5,6,7,8,9], False] for i in range(0,9)
                ] for j in range(0,9)
                ]

    def draw(self):
        """Docstring goes here
        """
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

    def init(self,path):
        """Docstring goes here
        """
        f = open(path)
        r = 0
        for l in f.readlines():
            vals = l.rstrip().split(',')
            for c in range(0,9):
                if int(vals[c]) != 0:
                    self.grid[r][c][0] = [int(vals[c])]
            r += 1
        f.close()

    def remove_value_cell(self,value,row,col):
        """Docstring goes here
        """
        if value in self.grid[row][col][0] and len(self.grid[row][col][0]) > 1:
            self.grid[row][col][0].remove(value)

    def remove_value_row(self,value,row):
        """Docstring goes here
        """
        for col in range(0,9):
            self.remove_value_cell(value,row,col)

    def remove_value_column(self,value,col):
        """Docstring goes here
        """
        for row in range(0,9):
            self.remove_value_cell(value,row,col)

    def remove_value_group(self,value,row,col):
        """Docstring goes here
        """
        y = 3 * floor(row/3)
        x = 3 * floor(col/3)
        rows = [i for i in range(y,y+3)]
        cols = [j for j in range(x,x+3)]
        for r in rows:
            for c in cols:
                self.remove_value_cell(value,r,c)

    # this function probably isn't necessary
    def ResetCheckFlags(self):
        for row in self.grid:
            for col in row:
                col[1] = False

    def check_cells(self):
        """Docstring goes here
        """
        foundmatch = False
        for row in range(0,9):
            for col in range(0,9):
                if len(self.grid[row][col][0]) == 1 and not self.grid[row][col][1]:
                    foundmatch = True
                    value = self.grid[row][col][0][0]
                    self.remove_value_column(value,col)
                    self.remove_value_row(value,row)
                    self.remove_value_group(value,row,col)
                    self.grid[row][col][1] = True
        return foundmatch

    def single_possibility_row(self):
        """Docstring goes here
        """
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

    def single_possiblity_column(self):
        """Docstring goes here
        """
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

    def single_possibility_group(self):
        """Docstring goes here
        """
        foundmatch = False
        for y in range(0,7,3):
            rows = [i for i in range(y,y+3)]
            for x in range(0,7,3):
                cols = [i for i in range(x,x+3)]
                missingValues = []
                seenValues = []
                for row in rows:
                    for col in cols:
                        if not self.grid[row][col][1]:
                            for val in self.grid[row][col][0]:
                                if val not in missingValues:
                                    missingValues.append(val)
                for row in rows:
                    for col in cols:
                        if not self.grid[row][col][1]:
                            for val in self.grid[row][col][0]:
                                if val not in seenValues:
                                    seenValues.append(val)
                                else:
                                    if val in missingValues:
                                        missingValues.remove(val)
                if len(missingValues) > 0:
                    foundmatch = True
                    for val in missingValues:
                        for row in rows:
                            for col in cols:
                                if val in self.grid[row][col][0]:
                                    self.grid[row][col][0] = [val]
        return foundmatch

    def naked_twin_row(self):
        """Docstring goes here
        """
        foundmatch = False
        for y in range(0,9):
            cellToCheck = []
            numCells = 0
            for x in range(0,9):
                if not self.grid[y][x][1]:
                    cellToCheck = self.grid[y][x][0]
                    numCells = 0
                    for i in range(0,9):
                        if self.grid[y][i][0] == cellToCheck:
                            numCells += 1
                    if numCells == len(cellToCheck):
                        foundmatch = True
                        for j in range(0,9):
                            if self.grid[y][j][0] != cellToCheck:
                                for val in cellToCheck:
                                    if val in self.grid[y][j][0]:
                                        self.remove_value_cell(val,y,j)
        return foundmatch

    def naked_twin_column(self):
        """Docstring goes here
        """
        foundmatch = False
        for x in range(0,9):
            cellToCheck = []
            numCells = 0
            for y in range(0,9):
                if not self.grid[y][x][1]:
                    cellToCheck = self.grid[y][x][0]
                    numCells = 0
                    for i in range(0,9):
                        if self.grid[i][x][0] == cellToCheck:
                            numCells += 1
                    if numCells == len(cellToCheck):
                        foundmatch = True
                        for j in range(0,9):
                            if self.grid[j][x][0] != cellToCheck:
                                for val in cellToCheck:
                                    if val in self.grid[j][x][0]:
                                        self.remove_value_cell(val,j,x)
        return foundmatch

    def naked_twin_group(self):
        """Docstring goes here
        """
        foundmatch = False
        for y in range(0,7,3):
            rows = [i for i in range(y,y+3)]
            for x in range(0,7,3):
                cols = [i for i in range(x,x+3)]
                cellToCheck = []
                numCells = 0
                for row in rows:
                    for col in cols:
                        if not self.grid[row][col][1]:
                            cellToCheck = self.grid[row][col][0]
                            numCells = 0
                            for i in rows:
                                for j in cols:
                                    if self.grid[i][j][0] == cellToCheck:
                                        numCells += 1
                            if numCells == len(cellToCheck):
                                foundmatch = True
                                for i in rows:
                                    for j in cols:
                                        if self.grid[i][j][0] != cellToCheck:
                                            for val in cellToCheck:
                                                if val in self.grid[i][j][0]:
                                                    self.remove_value_cell(val,i,j)
        return foundmatch

    def is_solved(self):
        """Docstring goes here
        """
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
s.init('sudoku.txt')
print('Initial grid:')
s.draw()
sleep(1)

# use the simple scanning algorithm first
while s.check_cells():
    system('cls')
    print('Scanning the grid...')
    s.draw()
    sleep(1)

# are we done?
if s.is_solved():
    print('\n\nSOLVED')
    exit()

keepgoing = True
while keepgoing: 
    keepgoing = False
    system('cls')
    print('Checking rows...')
    s.draw()
    if s.single_possibility_row():
        keepgoing = s.check_cells()
        system('cls')
        print('Checking rows...')
        s.draw()
        sleep(1)
    system('cls')
    print('Checking columns...') # remove...
    s.draw()
    if s.single_possiblity_column():
        keepgoing = s.check_cells()
        system('cls')
        print('Checking columns...') # remove...
        s.draw()
        sleep(1)
    system('cls')
    print('Checking groups...') # remove...
    s.draw()
    if s.single_possibility_group():
        keepgoing = s.check_cells()
        system('cls')
        print('Checking groups...') # remove...
        s.draw()
        sleep(1)

# use the scanning algorithm again
while s.check_cells():
    system('cls')
    print('Scanning the grid...')
    s.draw()
    sleep(1)
system('cls')
print('Scanning the grid...')
s.draw()

# are we done?
if s.is_solved():
    print('\n\nSOLVED')
    exit()

# look for matched cells
keepgoing = True
while keepgoing:
    keepgoing = False
    system('cls')
    print('Checking rows for matching cells...')
    s.draw()
    if s.naked_twin_row():
        keepgoing = s.check_cells()
        system('cls')
        print('Checking rows for matching cells...')
        s.draw()
        sleep(1)
    system('cls')
    print('Checking columns for matching cells...')
    s.draw()
    if s.naked_twin_column():
        keepgoing = s.check_cells()
        system('cls')
        print('Checking columns for matching cells...')
        s.draw()
        sleep(1)
    system('cls')
    print('Checking groups for matching cells...')
    s.draw()
    if s.naked_twin_group():
        keepgoing = s.check_cells()
        system('cls')
        print('Checking groups for matching cells...')
        s.draw()
        sleep(1)

# use the scanning algorithm again
while s.check_cells():
    system('cls')
    print('Scanning the grid...')
    s.draw()
    sleep(1)
system('cls')
print('Scanning the grid...')
s.draw()

# are we done?
if s.is_solved():
    print('\n\nSOLVED')
    exit()

print('\n\nI give up')
print('\nCell values:')
for row in s.grid:
    for col in row:
        print(col[0])