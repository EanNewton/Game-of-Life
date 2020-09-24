from random import choice
from time import sleep
from os import system, name
from sys import argv


def dead_state(width, height):
    return [[0] * width for _ in range(height)]


def random_state(width, height):
    return [[choice([0, 1]) for _ in range(width)] for _ in range(height)]


def next_board_state(board):
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


def render(board):
    edge = '{}\n'.format(''.join(['-' for _ in range(len(board[0]) + 2)]))
    banner = edge

    for row in board:
        newRow = '|'
        for column in row:
            newRow = '{}{}'.format(newRow, '#' if column else ' ')
        banner = '{}{}|\n'.format(banner, newRow)

    banner = '{}{}'.format(banner, edge)
    return banner


def load_file(filename):
    lines = list()
    if '.txt' in filename:
        with open('./pregens/{}'.format(filename), 'r') as f:
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


if __name__ == '__main__':
    if len(argv) == 2:
        board = load_file(argv[1])
        board = expand_board(board, 100, 50)
    elif len(argv) == 3:
        board = random_state(int(argv[1]), int(argv[2]))
    else:
        board = random_state(100, 50)
    
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
        board = next_board_state(board)

        if board in history:
            print('Reached end of life in {} cycles.'.format(lifespan))
            break
        
        sleep(0.1)