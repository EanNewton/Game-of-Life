from random import choice, choices
from time import sleep
from os import system, name
from sys import argv



def dead_state(width, height):
    return [[0] * width for _ in range(height)]


def random_state(width, height, deadWeight):
    liveWeight = 100 - deadWeight
    print(deadWeight, liveWeight)

    board = list()
    for _ in range(height):
        row = [choices([0, 1], weights=[deadWeight, liveWeight]) for _ in range(width)]
        board.append([each for sublist in row for each in sublist])

    return board


def next_board_state_conway(board):
    newBoard = dead_state(len(board[0]), len(board))

    for idxRow, row in enumerate(board, start=0):
        for idxCol, cell in enumerate(row, start=0):
            neighborCount = 0
            
            if idxCol - 1 >=  0 and board[idxRow][idxCol - 1]:
                neighborCount += 1

            if idxCol + 1 < len(board[idxRow]) and board[idxRow][idxCol + 1]:
                neighborCount += 1

            if idxRow - 1 >= 0 and board[idxRow - 1][idxCol]:
                neighborCount += 1
            
            if idxRow + 1 < len(board) and board[idxRow + 1][idxCol]:
                neighborCount += 1

            if idxRow + 1 < len(board) and idxCol + 1 < len(board[idxRow]) and board[idxRow + 1][idxCol + 1]:
                neighborCount += 1
                    
            if idxRow + 1 < len(board) and idxCol - 1 >= 0 and board[idxRow + 1][idxCol - 1]:
                neighborCount += 1

            if idxRow - 1 >= 0 and idxCol - 1 >= 0 and board[idxRow - 1][idxCol - 1]:
                neighborCount += 1

            if idxRow - 1 >= 0 and idxCol + 1 < len(board[idxRow]) and board[idxRow - 1][idxCol + 1]:
                neighborCount += 1

            #Rule 2
            if cell and (neighborCount == 2 or neighborCount == 3):
                newBoard[idxRow][idxCol] = 1
            #Rule 4
            elif not cell and neighborCount == 3:
                newBoard[idxRow][idxCol] = 1

    return newBoard


def next_board_state_brain(board):
    newBoard = dead_state(len(board[0]), len(board))

    for idxRow, row in enumerate(board, start=0):
        for idxCol, cell in enumerate(row, start=0):
            neighborCount = 0
            
            if idxCol - 1 >=  0 and board[idxRow][idxCol - 1] == 1:
                neighborCount += 1

            if idxCol + 1 < len(board[idxRow]) and board[idxRow][idxCol + 1] == 1:
                neighborCount += 1

            if idxRow - 1 >= 0 and board[idxRow - 1][idxCol] == 1:
                neighborCount += 1
            
            if idxRow + 1 < len(board) and board[idxRow + 1][idxCol] == 1:
                neighborCount += 1

            if idxRow + 1 < len(board) and idxCol + 1 < len(board[idxRow]) and board[idxRow + 1][idxCol + 1] == 1:
                neighborCount += 1
                    
            if idxRow + 1 < len(board) and idxCol - 1 >= 0 and board[idxRow + 1][idxCol - 1] == 1:
                neighborCount += 1

            if idxRow - 1 >= 0 and idxCol - 1 >= 0 and board[idxRow - 1][idxCol - 1] == 1:
                neighborCount += 1

            if idxRow - 1 >= 0 and idxCol + 1 < len(board[idxRow]) and board[idxRow - 1][idxCol + 1] == 1:
                neighborCount += 1

            #Rule 1: Dead cells come alive
            if not cell and neighborCount == 1:
                newBoard[idxRow][idxCol] = 1
            #Rule 2: Livings cells start dying
            elif cell == 1:
                newBoard[idxRow][idxCol] = 2
            #Rule 3: Turn off dying cells
            elif cell == 2:
                newBoard[idxRow][idxCol] = 0

    return newBoard


def next_board_state_langton(board, pos):
    x, y, direction = pos

        #if x < 0 or y < 0 or x == len(board[0]) or y == len(board):
        #   print('Reached edge of screen.')
            #quit()

    if x < 0:
        x = len(board[0]) - 1
    if y < 0:
        y = len(board)
    if x == len(board[0]):
        x = 0
    if y == len(board):
        y = 0

    if board[y][x]:
        direction += 90
        if direction == 360:
            direction = 0
        board[y][x] = 0
    else:
        direction -= 90
        if direction == -90:
            direction = 270
        board[y][x] = 1
        
    if direction == 0:
        y -= 1
    elif direction == 180:
        y += 1
    elif direction == 90:
        x += 1
    elif direction == 270:
        x -= 1

    return board, [x, y, direction]


def render(board):
    edge = '{}\n'.format(''.join(['-' for _ in range(len(board[0]) + 2)]))
    banner = edge

    for row in board:
        newRow = '|'
        for cell in row:
            if cell == 1:
                newRow = '{}{}'.format(newRow, '#')
            elif cell == 2:
                newRow = '{}{}'.format(newRow, '+')
            else:
                newRow = '{}{}'.format(newRow, ' ')
        banner = '{}{}|\n'.format(banner, newRow)

    banner = '{}{}'.format(banner, edge)
    return banner


def load_file(filename):
    lines = list()
    if '.txt' in filename:
        with open('./pregens/{}.txt'.format(filename), 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                try:
                    lines.append([int(cell) for cell in line.strip()])
                except ValueError:
                    print('Invalid character detected. All characters must be 0 or 1.')
                    quit()
    
    return lines


def expand_board(board, width, height):
    while len(board) < height:
        board.append([0])
    for row in board:
        while len(row) < width:
            row.append(0)
    return board


def langton(board, pos):
    lifespan = 0
    while True:
        system('cls' if name == 'nt' else 'clear')
        banner = render(board)
        print(banner)
        print('Cycle:  {}'.format(lifespan + 1))
        
        lifespan += 1
        if type(pos[0]) is list:
            for idx, each in enumerate(pos):
                board, pos[idx] = next_board_state_langton(board, each)
        else:
            board, pos = next_board_state_langton(board, pos)
        sleep(0.05)


def brain(board):
    lifespan = 0
    while True:
        system('cls' if name == 'nt' else 'clear')
        banner = render(board)
        print(banner)
        print('Cycle:  {}'.format(lifespan + 1))

        lifespan += 1
        board = next_board_state_brain(board)

        sleep(0.5)


def conway(board):
    lifespan = 0
    history = [None, None]
    while True:
        system('cls' if name == 'nt' else 'clear')
        banner = render(board)
        print(banner)
        print('Cycle:  {}'.format(lifespan + 1))

        if lifespan % 2 == 0:
            history[0] = board
        else:
            history[1] = board
        lifespan += 1
        board = next_board_state_conway(board)

        if board in history:
            print('Reached end of life in {} cycles.'.format(lifespan))
            break
        
        sleep(0.1)


if __name__ == '__main__':
    help = """
    Cell Automata.
    
    Usage:
        Conways Game of Life
        ====================
        main.py conway
        main.py conway <filename>
        main.py conway <width> <height> <density>

        Langton's Ant
        =============
        main.py ant
        main.py ant <width> <height> <density>
        main.py ant <width> <height> <density> <workers>

        Brian's Brain
        =============
        main.py brain
        main.py brain <filename>
        main.py brain <width> <height>
        main.py brain <width> <height> <density>

    Options:
        <filename> -- a .txt file located in ./pregens
        <width>    -- X cell range
        <height>   -- Y cell range
        <density>  -- percent chance to spawn a living cell at start, between 0 and 100
        <workers>  -- number of simultaneous ants on the board
    """
    if 'help' in argv:
        print(help)
        quit()

    elif len(argv) >= 2:
        if argv[1] == 'conway':
            if len(argv) == 3:
                board = load_file(argv[2])
                board = expand_board(board, 50, 25)
            elif len(argv) == 5:
                board = random_state(int(argv[2]), int(argv[3]), int(argv[4]))
            else:
                board = random_state(50, 25, 50)
            conway(board)

        elif argv[1] == 'ant':
            if len(argv) == 6:
                board = random_state(int(argv[2]), int(argv[3]), int(argv[4]))
                pos = list()
                for _ in range(int(argv[5])):
                    pos.append([
                        choice(range(1, len(board[0]) - 2)),
                        choice(range(1, len(board) - 2)),  
                        choice([0, 90, 180, 270])
                        ])
            elif len(argv) == 5:
                board = random_state(int(argv[2]), int(argv[3]), int(argv[4]))
                pos = [
                    choice(range(1, len(board[0]) - 2)),
                    choice(range(1, len(board) - 2)),  
                    choice([0, 90, 180, 270])
                    ]
            else:
                board = random_state(50, 25, 50)
            langton(board, pos)
            
        elif argv[1] == 'brain':
            if len(argv) == 3:
                board = load_file(argv[2])
                board = expand_board(board, 50, 25)
            elif len(argv) == 4:
                board = random_state(int(argv[2]), int(argv[3]), 50)
            elif len(argv) == 5:
                board = random_state(int(argv[2]), int(argv[3]), int(argv[4]))
            else:
                board = random_state(50, 25, 50)
            brain(board)
    print(help)


