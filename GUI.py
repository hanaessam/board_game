import pygame
import numpy as np

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
i = 7
COLUMN_COUNT = i

SQUARESIZE = 95   #pixels
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

EMPTY = 0
AI_1_PIECE = 1
AI_2_PIECE = 2

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# (0,0) for us is the left down piece but in matrix it is the left upper piece, so we flip over x-axis
def print_board(board):
    print(np.flip(board, 0))

def draw_board(board):
    # draw the empty initial board first
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # add in the players pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == AI_1_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_2_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def easy():
    board = create_board()
    print_board(board)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Connect 4')
    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 75)
    draw_board(board)
    print("Easy")


def hard():
    print("Hard")


def button(screen, position, text, size, colors="black on white"):
    fg, bg = colors.split(" on ")
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, 1, fg)
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, bg, (x, y, w, h))
    print(screen.blit(text_render, (x, y)))
    return screen.blit(text_render, (x, y))


def menu():
    b0 = button(screen, (150, 10), "Choose Level", 55, "black on white")
    b1 = button(screen, (150, 150), "Easy", 50, "red on yellow")
    b2 = button(screen, (350, 150), "Hard", 50, "red on yellow")
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check when you click if the coordinates of the pointer are in the rectangle of the buttons
                if b1.collidepoint(pygame.mouse.get_pos()):
                    easy()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    hard()
        pygame.display.update()
    pygame.quit()


pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Connect 4')
menu()
