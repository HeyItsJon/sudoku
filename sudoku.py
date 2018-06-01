from time import sleep

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.value = [1,2,3,4,5,6,7,8,9]
        self.checked = False

'''
open file
create 81 Cell objects - row 1-9, column 1-9
put Cell objects in list?
go through file and set Cell.value for the known cells
while not solved:
    loop through rows
        loop through columns
            if Cell.value is a single value
                go through cells in row and remove that value
                go through cells in column and remove that value
                find cells in 3x3 block and remove that value
    check if we're solved
    (maybe add in a flag to check if we've gone through each Cell without modifying one - hit a dead end)
(additional logic?)
'''

def CheckIfSolved(grid):
    pass

def DrawGrid(grid):
    print(' _______________________ ')
    print('|       |       |       |')
    for x in range(0,9):
        tmp = '| '
        for y in range(0,9):
            for c in grid:
                if (c.row == x and c.col == y):
                    if len(c.value) == 1:
                        tmp += (str(c.value))[1] + ' '
                    else:
                        tmp += '  '
            if y == 2 or y == 5:
                tmp += '| '
        tmp += '|'
        print(tmp)
        if x == 2 or x == 5:
            print('|_______|_______|_______|')
            print('|       |       |       |')
    print('|_______|_______|_______|')

def InitializeGrid(grid):
    f = open('sudoku.txt')
    row = 0
    for l in f.readlines():
        vals = l.rstrip().split(',')
        for col in range(0,9):
            if int(vals[col]) != 0:
                for c in grid:
                    if(c.row == row and c.col == col):
                        c.value = [int(vals[col])]
        row +=1 
    f.close()
    return grid

def RemoveValue(grid, cell):
    value = cell.value[0]
    # brute force it...
    if cell.row < 3:
        rows = [0,1,2]
    elif cell.row < 6:
        rows = [3,4,5]
    else:
        rows = [6,7,8]
    if cell.col < 3:
        cols = [0,1,2]
    elif cell.col < 6:
        cols = [3,4,5]
    else:
        cols = [6,7,8]

    # remove from common row and column
    for i in range(0, len(grid)):
        if (grid[i].row == cell.row or grid[i].col == cell.col) and len(grid[i].value) != 1:
            grid[i].value.remove(value)
    
    # remove from 3x3 square
    for row in rows:
        for col in cols:
            for i in range(0, len(grid)):
                if (grid[i].row == row or grid[i].col == col) and len(grid[i].value) != 1:
                    print(str(row) + ',' + str(col) + ': ' + str(value))
                    grid[i].value.remove(value)

    return grid

g = []
for x in range(0,9):
    for y in range(0,9):
        c = Cell(x,y)
        g.append(c)

# intialize grid from provided txt file
g = InitializeGrid(g)
DrawGrid(g)
sleep(1)

# start with a simple algorithm
# for each cell in g
#   check if .checked = false
#   if false
#       RemoveValue(row, col)
for c in g:
    if not c.checked:
        g = RemoveValue(g, c)
        DrawGrid(g)
        sleep(1)



