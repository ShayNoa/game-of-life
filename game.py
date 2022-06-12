import sys
from typing import Generator, NamedTuple

import numpy as np
import pygame

# cell modes
ALIVE = 1
DEAD = 0

SIZE = 50
WIDTH = SIZE * 10
HEIGHT = SIZE * 10
PIX_NUM = WIDTH / SIZE
FPS = 10

# pygame colors
BACKGROUND = (30, 30, 30)
CELLS = (27, 185, 33, 0)

class Cell(NamedTuple):
    num: int
    r_index: int
    c_index: int
    neighbors: int

def generate_board(SIZE: int) -> np.ndarray:
    board = np.random.randint(0, 2, size=(SIZE, SIZE))
    return board
    

def update_board(board: np.ndarray) -> np.ndarray:
    set_alive = 3
    lower_limit, upper_limit = 2, 3
    board_copy = np.copy(board)
    for cell in check_neighbors(board):
        if cell.num:
            if lower_limit <= cell.neighbors <= upper_limit:
                board_copy[cell.r_index][cell.c_index] = ALIVE
            else:
                board_copy[cell.r_index][cell.c_index] = DEAD
        if not cell.num and cell.neighbors == set_alive:
            board_copy[cell.r_index][cell.c_index] = ALIVE
    return board_copy


def check_neighbors(board: np.ndarray):
    offset = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), 
                (1, 0), (1, -1), (0, -1)]
    for (r_index, c_index), num in np.ndenumerate(board):
        neighbors = 0
        for x, y in offset:
            row = r_index + x
            col = c_index + y
            if 0 <= row < SIZE and 0 <= col < SIZE:
                cell = board[row][col]
                neighbors += cell
        yield Cell(num, r_index, c_index, neighbors)


def draw_board(board: np.ndarray, screen: pygame.surface.Surface) -> None:
    screen.fill(BACKGROUND)
    for (r_index, c_index), num in np.ndenumerate(board):
        if num:
            pygame.draw.rect(screen, CELLS, [(r_index * PIX_NUM), (c_index * PIX_NUM), 10, 10])
    pygame.display.flip()


def main(board: np.ndarray):  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        updated_board = update_board(board)
        board = updated_board
        clock.tick(FPS)      
        draw_board(board, screen)
       

if __name__ == "__main__":
    board = generate_board(SIZE)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    main(board)




