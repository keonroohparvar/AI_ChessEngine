"""
Monte Carlo implementation that will be the way our Chess Engine is able
to go down potential moves and choose the best one.

Author: Sammy Paykel
Date: 4/19/2023
"""

# Imports
import os
import sys

import tensorflow as tf
import numpy as np

# Local imports
from board import ChessBoard


def example_use_of_model(model_path, board):
    # We will print out board to see what our board looks like
    print('Our starting board is ... ')
    board.print_board()
    print('\n-------\n')

    # We will get the list of all available, legal moves
    legal_moves = list(board.get_legal_moves())

    """
    This is demonstrating how we make a move. 
    """
    # First, we will get the original FEN as we need it to
    # revert to our original board after we make a move.
    original_FEN = board.get_fen()

    # Let's get an example move by chosing the first legal move from our list
    example_move = legal_moves[0]
    print("An example of a move is - ", str(example_move))
    print('\n-------\n')

    # Let's alter the board and make that move
    board.make_move(str(example_move))
    print('The new board is seen below...')
    board.print_board()
    print('\n-------\n')

    # Now, let's bring our board back to its original state
    board.set_fen(original_FEN)

    """
    This is how to use a model to predict the quality of a board.
    """
    # Let's look at the path to a model. NOTE: it should be an .h5 file
    print('Our path to our model is - ', model_path)
    print('\n-------\n')

    # Let's load in our model using tensorflow
    model = tf.keras.models.load_model(model_path)

    # Let's have our model predict on a board. First, you need to positionally encode our board.
    board_encoding = board.positional_encode()

    # Now, let's predict on our board. NOTE: to predict on a board, you need to wrap up
    # the board positional encoding in a numpy array (ask me if this doesn't make sense)
    prediction = model.predict(np.array([board_encoding]), verbose=0)[0][0]
    print('The model predicts that the board evaluation is ', prediction)
    print('\n-------\n')

def white_monte(legal_moves, original_FEN, model):
    curr_best_move_num = -100
    curr_best_move = ""

    for move in legal_moves:
        board.make_move(str(move))

        board_encoding = board.positional_encode()
        prediction = model.predict(np.array([board_encoding]), verbose=0)[0][0]

        if (prediction > curr_best_move_num):
            curr_best_move_num = prediction
            curr_best_move = str(move)

        board.set_fen(original_FEN)

    return curr_best_move, curr_best_move_num

def black_monte(legal_moves, original_FEN, model):
    curr_best_move_num = 100
    curr_best_move = ""
    for move in legal_moves:
        board.make_move(str(move))

        board_encoding = board.positional_encode()
        prediction = model.predict(np.array([board_encoding]), verbose=0)[0][0]

        if (prediction < curr_best_move_num):
            curr_best_move_num = prediction
            curr_best_move = str(move)

        board.set_fen(original_FEN)

    return curr_best_move, curr_best_move_num

'''
# This was an experiment i was doing in a depth = 2 monte carlo
def monte_carlo_two(model_path, board, turn):
    model = tf.keras.models.load_model(model_path)

    legal_moves_1 = list(board.get_legal_moves())
    original_FEN = board.get_fen()

    if turn == "white":
        turn_2 = "black"
    else:
        turn_2 = "white"

    for move in legal_moves_1:
        board.make_move(str(move))

        legal_moves_2 = list(board.get_legal_moves())
        FEN_2 = board.get_fen()

        best_2 = ""
        best_2_num = 0

        for move_2 in legal_moves_2:
            if turn_2 == "white":
                best_2, best_2_num = white_monte(legal_moves_2, original_FEN, model)
            else:
                best_2, best_2_num = black_monte(legal_moves_2, original_FEN, model)
'''


def mc_eval_board(turn, board, current_depth, max_depth):
    """
    this is the recursive function that will eval a board.
    NOTE: this probably doesn't work but this is close I think haha I did not test this sorry my kings
    """
    model_path = '../models/keon/saved_models/model_example.h5'
    model = tf.keras.models.load_model(model_path)

    # Function for switching turns
    def switch_turn(turn):
        if turn == 'W':
            return 'B'
        else:
            return 'W'

    # Get current evaluation
    board_encoding = board.positional_encode()
    curr_eval = model.predict(np.array([board_encoding]), verbose=0)[0][0] # evaluation of the "board" parameter

    # CHECK IF WE ARE AT MAX DEPTH - IF WE DON'T DO THIS, WE RECURSE FOREVER
    if max_depth == current_depth:
        return curr_eval # evaluation of our current board

    # Get all possible boards
    legal_moves = list(board.get_legal_moves())
    original_FEN = board.get_fen()
    possible_boards = []  # list of all possible boards that can be made at moment
    for move in legal_moves:
        board.make_move(str(move))
        possible_boards.append(board)
        board.set_fen(original_FEN)

    # Handle cases differently for both teams ->

    # If turn is W, we will return the max of the options (because white wants to maximize)
    if turn == 'W':
        other_turn = 'B'
        return curr_eval + max([mc_eval_board(other_turn, i, current_depth + 1, max_depth) for i in possible_boards])

    # If turn is B, we will return the min of the options (because black wants to minimize)
    if turn == 'B':
        other_turn = 'W'
        return curr_eval + min([mc_eval_board(other_turn, i, current_depth + 1, max_depth) for i in possible_boards])


def monte_carlo(board, max_depth):
    turn = 'W'  # if we are white, 'B' else

    # --- GO through all the boards ---

    legal_moves = list(board.get_legal_moves())
    original_FEN = board.get_fen()

    possible_boards = []  # list of all possible boards that can be made at moment
    for move in legal_moves:
        board.make_move(str(move))
        possible_boards.append(board)
        board.set_fen(original_FEN)

    # --- GO through possibilities and do MCTS ---

    values = []
    for poss_board in possible_boards:
        this_value = mc_eval_board(turn, poss_board, current_depth=0, max_depth=max_depth)
        values.append(this_value)

    # Choose the board that yields the highest value
    best_board = max(values)
    return best_board


if __name__ == '__main__':
    board = ChessBoard()
    # model_path = '../models/keon/saved_models/model_example.h5'
    # example_use_of_model(model_path, board)
    # board.make_move("g1h3")
    # board.make_move("g8h6")
    # print(monte_carlo_two(model_path, board, "white"))
    print(monte_carlo(board, 2))
