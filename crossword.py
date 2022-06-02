from re import *

def solve_crossword(grid, cell):
    # base case for the recursion
    if solved(grid):
        return True

    # dimensions of the cell
    row = cell[0]
    col = cell[1]

    # get dimensions of the next cell
    next_cell = get_next_cell(grid, cell)

    # solve the next cell if the current is a blank cell
    if grid[row][col] == ' ' or grid[row][col] in domain:
        return solve_crossword(grid, next_cell)

    # assign value to the cell if it's not a blank cell
    if grid[row][col] == '#':
        for value in domain:
            # check whether the value satisfy the constraints
            if is_valid(grid, cell, value):
                # assign the value to the cell
                grid[row][col] = value
                # search for solution for the next cell
                # if there is a solution for the next cell continue to the next...
                if solve_crossword(grid, next_cell):
                    return True
                # if not backtrack
                else:
                    grid[row][col] = '#'
    grid[row][col] = '#'
    return False


# check if the value satisfy the constraints
def is_valid(grid, cell, value):
    # dimensions of the cell
    row = cell[0]
    col = cell[1]

    # assign value to the current cell
    grid[row][col] = value

    # return all possible tracks
    get_all_tracks(grid)

    for track in tracks:
        # check if the cell exist in the track
        if cell in track.keys():
            # put new line at the beginning and the end to match the words in the dictionary
            regex = '\n'
            # construct the word (regex) to search for it in the dictionary ex. it would be => a.....
            for value in track.values():
                if value in domain:
                    regex += value
                elif value == '#':
                    regex += '.'
            regex += '\n'
            # if the word does not exist in the dictionary, or it is already taken, that violate the constraints
            if search(regex, words) == None or regex in word_taken:
                return False
            # word that complete the cells of the track and satisfy the constraints
            if '.' not in regex:
                word_taken.append(regex)
    return True

def get_all_tracks(grid):
    global tracks
    global visitedx
    global visitedy
    tracks = []
    visitedx = []
    visitedy = []

    for i in range (len(grid[0])):
        for j in range(len(grid)):
            if grid[i][j] != ' ':
                get_cell_tracks(grid, (i, j))

def get_cell_tracks(grid, cell):
    row = cell[0]
    col = cell[1]
    # Check if the cell is inside the boundary of the crossword and not visited horizontally
    if col + 1 < len(grid[0]) and \
        grid[row][col + 1] != ' ' and \
        cell not in visitedx:
            tracks.append(complete_right(grid, cell))

    # Check if the cell is inside the boundary of the crossword and not visited vertically
    if row + 1 < len(grid) and \
        grid[row + 1][col] != ' ' and \
        cell not in visitedy:
            tracks.append(complete_down(grid, cell))

def get_next_cell(grid, cell):
    # dimensions of the current cell
    row = cell[0]
    col = cell[1]

    col += 1
    # if the value of the column is more than the width of the crossword go to the next row
    if col == len(grid[0]):
        col = 0
        row += 1
    return (row, col)


# check for complete assignment
def solved(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            if grid[i][j] == '#':
                return False
    return True


# get horizontal track
def complete_right(grid, cell):
    row = cell[0]
    col = cell[1]
    track = {}

    # append cells with its values to track while the column of the cell has not exceeded the boundary
    while col < (len(grid[0])) and \
        grid[row][col] != ' ':
            track[(row, col)] = grid[row][col]
            visitedx.append((row, col))
            col += 1
    return track

# get vertical track
def complete_down(grid, cell):
    row = cell[0]
    col = cell[1]
    track = {}

    # append cells with its values to track while the row of the cell has not exceeded the boundary
    while row < len(grid) and \
        grid[row][col] != ' ':
            track[(row, col)] = grid[row][col]
            visitedy.append((row, col))
            row += 1
    return track


if __name__ == '__main__':

    # crossword to get solved
    grid = [
        ['#', '#', '#', '#', '#'],
        ['e', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', '#'],
        [' ', ' ', '#', ' ', '#']
    ]

    # open dictionary
    f = open("words.txt")
    words = f.read()

    domain = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    word_taken = []

    # check for solution
    if not (solve_crossword(grid, (0, 0))):
        print ('There is no solution!')

    else:
        print('SOLVED CROSSWORD: ')
        for row in grid:
            print((5*' '), row)

        print(20*'-')

        # print the words that solve the crossword
        print('WORDS:')
        for word in word_taken:
            print((5*' '), word[1:-1])
