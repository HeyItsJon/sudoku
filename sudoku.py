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

# i am making changes

def CheckIfSolved(grid):
    pass

def DrawGrid(grid):
    print(' _______________________ ')
    print('|       |       |       |')
    for x in range(1,10):
        tmp = '| '
        for y in range(1,10):
            for c in grid:
                if (c.row == x and c.col == y):
                    if len(c.value) == 1:
                        tmp += (str(c.value))[1] + ' '
            if y == 3 or y == 6:
                tmp += '| '
        tmp += '|'
        print(tmp)
        if x == 3 or x == 6:
            print('|_______|_______|_______|')
            print('|       |       |       |')
    print('|_______|_______|_______|')

g = []
for x in range(1,10):
    for y in range(1,10):
        c = Cell(x,y)
        c.value = [x]
        g.append(c)
DrawGrid(g)
