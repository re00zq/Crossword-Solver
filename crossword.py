from re import *
f = open("words.txt")
words = f.read()
word_taken = []
grid = [['#', '#', '#', '#', '#'],
        ['#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', '#'],
        ['#', ' ', '#', ' ', '#'],
        ['#', '#', '#', ' ', '#']]

domain = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
tracks = []
visitedx = []; visitedy = []

def complete_right(grid, cell):
    row = cell[0]
    col = cell[1]
    track = {} 
    while col < len(grid[0]) and (grid[row][col] != ' '):
        track[(row, col)] = grid[row][col]
        visitedx.append((row, col))
        col += 1
    return track    


def complete_down(grid, cell):
    row = cell[0]
    col = cell[1]
    track = {}
    while row < len(grid) and (grid[row][col] != ' '):
        track[(row, col)] = grid[row][col]
        visitedy.append((row, col))
        row += 1
    return track  


def get_cell_tracks(grid, cell):
    row = cell[0]
    col = cell[1]

    if col + 1 < len(grid[0]) and grid[row][col + 1] != ' ' and cell not in visitedx:
        tracks.append(complete_right(grid, cell))

    if row + 1 < len(grid) and grid[row + 1][col] != ' ' and cell not in visitedy:
        tracks.append(complete_down(grid, cell))
    



def get_all_tracks(grid):
    global tracks
    global visitedx
    global visitedy
    tracks = []
    visitedx = []
    visitedy = []
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            if grid[i][j] != ' ':
                get_cell_tracks(grid, (i, j))  


def get_next_cell(grid, cell):
    row = cell[0]; col = cell[1]
    col += 1
    if col == len(grid[0]):
        col = 0
        row += 1
    return (row, col)


def is_valid(grid, cell, value):
    row = cell[0]; col = cell[1]
    grid[row][col] = value
    get_all_tracks(grid)
    
    for track in tracks:
        
        if cell in track.keys():
            regex = '\n'
            for value in track.values():
                if value in domain: regex += value
                elif value == '#': regex += '.'
            regex += '\n'  
            if search(regex, words) == None or regex in word_taken:
                return False
            if '.' not in regex:
                word_taken.append(regex)    
    return True


def solved(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            if grid[i][j] == '#':
                return False
    return True


def solve_crossword(grid, cell):

    if solved(grid): return True

    row = cell[0]; col = cell[1]
    next_cell = get_next_cell(grid, cell)

    if grid[row][col] == ' ':
        return solve_crossword(grid, next_cell)
    
    if grid[row][col] == '#':
        
        for value in domain:
            if is_valid(grid, cell, value):
                grid[row][col] = value
                if solve_crossword(grid, next_cell): return True
                else:
                    grid[row][col] = '#'
                    
    grid[row][col] ='#'
    return False


print(solve_crossword(grid, (0,0)))
print('\n', 20*'#', '\n')

for row in grid:
    print(row)
print('\n', 20*'#', '\n')

for word in word_taken:
    print(word[1:-1])