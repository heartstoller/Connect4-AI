import pygame as conui
import sys
import math
import random
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox

#constants
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

#initialize conui
conui.init()

#set up display
screen = conui.display.set_mode(SIZE)
conui.display.set_caption("Connect 4")

#font for winner message
myfont = conui.font.SysFont("monospace", 75)

#create gameboard
def create_connect4():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

#drop piece into the gameboard
def drop_ball(gameboard, row, col, piece):
    gameboard[row][col] = piece

#check for valid column
def check_valid_location(gameboard, col):
    return gameboard[ROW_COUNT - 1][col] == 0

#get next open row in a column
def get_next_open_row(gameboard, col):
    for r in range(ROW_COUNT):
        if gameboard[r][col] == 0:
            return r

def draw_connect4(gameboard):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            #draw the background grid
            conui.draw.rect(
                screen,
                (0, 0, 255),  #blue color for the gameboard background
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            #draw empty circles for slots
            conui.draw.circle(
                screen,
                (0, 0, 0),  #black color for empty slots
                (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE)),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if gameboard[r][c] == PLAYER_PIECE:
                #draw red circles for player pieces
                conui.draw.circle(
                    screen,
                    (255, 0, 0),  #red color for player pieces
                    (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS,
                )
            elif gameboard[r][c] == AI_PIECE:
                #draw yellow circles for AI pieces
                conui.draw.circle(
                    screen,
                    (255, 255, 0),  #yellow color for AI pieces
                    (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS,
                )
    #update display to show changes
    conui.display.update()

    
def score_position(gameboard1, piece):
    score = 0
    opponent_piece = 1 if piece == 2 else 2
    
    #center column weighting
    center_column = [int(i) for i in list(gameboard1[:, COLUMN_COUNT//2])]
    center_count = center_column.count(piece)
    score += center_count * 3  #reward for controlling the center

    #horizontal scoring
    for row in gameboard1:
        row_array = [int(i) for i in list(row)]
        for col in range(COLUMN_COUNT - 3):
            window = row_array[col:col + 4] #sliding window
            score += evaluate_window(window, piece, opponent_piece)

    #vertical scoring
    for col in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(gameboard1[:, col])]
        for row in range(ROW_COUNT - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, piece, opponent_piece)

    # Diagonal scoring
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [gameboard1[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, piece, opponent_piece)

        for col in range(3, COLUMN_COUNT):
            window = [gameboard1[row+i][col-i] for i in range(4)]
            score += evaluate_window(window, piece, opponent_piece)

    return score

def evaluate_window(window, piece, opponent_piece):
    score = 0
    if window.count(piece) == 4:  #winning window
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:  #almost winning
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:  #potential streak
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1:  #block opponent
        score -= 4
    return score




def winningmove(gameboard, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(gameboard[r][c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(gameboard[r + i][c] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(gameboard[r + i][c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(gameboard[r - i][c + i] == piece for i in range(4)):
                return True
    return False

#monte carlo AI move selection
'''def monte_carlo(gameboard, piece, simulations=100):
    scores = {col: 0 for col in range(COLUMN_COUNT)}

    for col in range(COLUMN_COUNT):
        if check_valid_location(gameboard, col):
            temp_gameboard = gameboard.copy()
            for _ in range(simulations):
                temp_gameboard_copy = temp_gameboard.copy()
                drop_ball(temp_gameboard_copy, get_next_open_row(temp_gameboard_copy, col), col, piece)
                if winningmove(temp_gameboard_copy, piece):
                    scores[col] += 100
                else:
                    scores[col] += random.randint(0, 10)

    return max(scores, key=scores.get)'''

def monte_carlo(gameboard, piece, simulations=100):
    def simulate_game(temp_board, piece):
        """
        Play a random game until the end and return the result.
        """
        turn = piece
        while True:
            valid_columns = [col for col in range(COLUMN_COUNT) if check_valid_location(temp_board, col)]
            if not valid_columns:
                return 0  #draw if no moves left
            col = random.choice(valid_columns)
            row = get_next_open_row(temp_board, col)
            drop_ball(temp_board, row, col, turn)
            if winningmove(temp_board, turn):
                return 1 if turn == piece else -1  #win or loss
            turn = PLAYER_PIECE if turn == AI_PIECE else AI_PIECE

    scores = {col: 0 for col in range(COLUMN_COUNT)}

    for col in range(COLUMN_COUNT):
        if check_valid_location(gameboard, col):
            for _ in range(simulations):
                temp_board = gameboard.copy()
                row = get_next_open_row(temp_board, col)
                drop_ball(temp_board, row, col, piece)
                if winningmove(temp_board, piece):
                    scores[col] += 1  #immediate win
                else:
                    scores[col] += simulate_game(temp_board, AI_PIECE)

    return max(scores, key=scores.get)

#select difficulty using a dialog box
def select_difficulty():
    root = tk.Tk()
    root.withdraw()
    difficulty = simpledialog.askstring("Select Difficulty", "Choose difficulty: easy, medium, hard")
    if difficulty not in ["easy", "medium", "hard"]:
        messagebox.showinfo("Invalid Input", "Defaulting to 'medium'.")
        difficulty = "medium"
    return difficulty

#ask if the user wants to retry
def ask_retry():
    root = tk.Tk()
    root.withdraw()
    return messagebox.askyesno("Retry", "Do you want to play again?")

def validlocation(gameboard1):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if check_valid_location(gameboard1, col):
            valid_locations.append(col)
    return valid_locations

def isleaf_node(gameboard1):
    return winningmove(gameboard1, PLAYER_PIECE) or winningmove(gameboard1, AI_PIECE) or len(validlocation(gameboard1)) == 0

def minimax(gameboard1, depth, alpha, beta, maximizingPlayer):
    valid_locations = validlocation(gameboard1)
    if valid_locations==[]:
        conui.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, SQUARESIZE))
        label = myfont.render("AI Wins!", 1, (255, 255, 0))
        screen.blit(label, (40, 10))
        ask_retry(gameboard1)

    is_terminal = isleaf_node(gameboard1)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winningmove(gameboard1, AI_PIECE):
                return (None, 100000000000000)
            elif winningmove(gameboard1, PLAYER_PIECE):
                return (None, -10000000000000)
            else: 
                return (None, 0)
        else:
            return (None, score_position(gameboard1, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(gameboard1, col)
            temp_gameboard1 = gameboard1.copy()
            drop_ball(temp_gameboard1, row, col, AI_PIECE)
            score = minimax(temp_gameboard1, depth-1, alpha, beta, False)[1]
            if score > value:
                value = score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(gameboard1, col)
            temp_gameboard1 = gameboard1.copy()
            drop_ball(temp_gameboard1, row, col, PLAYER_PIECE)
            score = minimax(temp_gameboard1, depth-1, alpha, beta, True)[1]
            if score < value:
                value = score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    
#main game logic
def main():
    gameboard = create_connect4()
    draw_connect4(gameboard)
    conui.display.update()

    turn = random.randint(PLAYER_PIECE, AI_PIECE)
    game_over = False
    difficulty = select_difficulty()

    while not game_over:
        for event in conui.event.get():
            if event.type == conui.QUIT:
                sys.exit()

            if event.type == conui.MOUSEMOTION:
                conui.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER_PIECE:
                    conui.draw.circle(screen, (255, 0, 0), (posx, int(SQUARESIZE / 2)), RADIUS)
                conui.display.update()

            if event.type == conui.MOUSEBUTTONDOWN:
                if turn == PLAYER_PIECE:
                    col = event.pos[0] // SQUARESIZE
                    if check_valid_location(gameboard, col):
                        row = get_next_open_row(gameboard, col)
                        drop_ball(gameboard, row, col, PLAYER_PIECE)

                        if winningmove(gameboard, PLAYER_PIECE):
                            label = myfont.render("Player Wins!", 1, (255, 0, 0))
                            screen.blit(label, (40, 10))
                            conui.display.update()
                            conui.time.wait(3000)
                            game_over = True

                        turn = AI_PIECE
                        draw_connect4(gameboard)

            if turn == AI_PIECE and not game_over:
                conui.time.wait(500)
                if difficulty == "easy":
                    col = random.choice([c for c in range(COLUMN_COUNT) if check_valid_location(gameboard, c)])
                elif difficulty == "medium":
                    col = monte_carlo(gameboard, AI_PIECE, simulations=100)
                elif difficulty == "hard":
                    col, _ = minimax(gameboard, 5, -math.inf, math.inf, True)

                if check_valid_location(gameboard, col):
                    row = get_next_open_row(gameboard, col)
                    drop_ball(gameboard, row, col, AI_PIECE)

                    if winningmove(gameboard, AI_PIECE):
                        label = myfont.render("AI Wins!", 1, (255, 255, 0))
                        screen.blit(label, (40, 10))
                        conui.display.update()
                        conui.time.wait(3000)
                        game_over = True

                    draw_connect4(gameboard)
                    turn = PLAYER_PIECE

        if game_over:
            if ask_retry():
                main()
            else:
                sys.exit()

if __name__ == "__main__":
    main()
