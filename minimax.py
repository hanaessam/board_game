import math
import random

import numpy as np  # to help in making our matrix for problem representation
import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
i = 7
COLUMN_COUNT = i

AI_1 = 0
AI_2 = 1

EMPTY = 0
AI_1_PIECE = 1
AI_2_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 95  # pixels
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# check that the column is not filled
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece


# (0,0) for us is the left down piece but in matrix it is the left upper piece, so we flip over x-axis
def print_board(board):
    print(np.flip(board, 0))


# check if this move will make you win
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = AI_1_PIECE
    if piece == AI_1_PIECE:
        opp_piece = AI_2_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, AI_1_PIECE) or winning_move(board, AI_2_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, maximizingPlayer, player):
    if player == AI_1:
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, AI_1_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, AI_2_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, score_position(board, AI_1_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = -1
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_1_PIECE)
                new_score = minimax(b_copy, depth - 1, False, player)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_2_PIECE)
                new_score = minimax(b_copy, depth - 1, True, player)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

    elif player == AI_2:
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, AI_2_PIECE):
                    return (None, 100000000000000)
                elif winning_move(board, AI_1_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, score_position(board, AI_2_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = -1
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_2_PIECE)
                new_score = minimax(b_copy, depth - 1, False, player)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_1_PIECE)
                new_score = minimax(b_copy, depth - 1, True, player)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = -1
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()  # so that any modifications doesn't affect the original board
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


# GUI
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
    game_over = False

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Connect 4')
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(AI_1, AI_2)

    while not game_over:
        # Player 1 Input
        if turn == AI_1 and not game_over:
            col, minimax_score = minimax(board, 5, True, AI_1)

            if is_valid_location(board, col):
                pygame.time.wait(300)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_1_PIECE)

                if winning_move(board, AI_1_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)

        # Player 2 Input
        elif turn == AI_2 and not game_over:
            col, minimax_score = minimax(board, 5, True, AI_2)

            if is_valid_location(board, col):
                pygame.time.wait(300)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_2_PIECE)

                if winning_move(board, AI_2_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)
        if game_over:
            pygame.time.wait(3000)   # wait 3 sec and shut down automatically
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
    # print(screen.blit(text_render, (x, y)))
    return screen.blit(text_render, (x, y))


def menu():
    b0 = button(screen, (150, 10), "Choose Level", 55, "black on white")
    b1 = button(screen, (150, 150), "Easy", 50, "red on yellow")
    b2 = button(screen, (350, 150), "Hard", 50, "red on yellow")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
pygame.display.set_caption('Connect 4 (minimax)')
menu()
