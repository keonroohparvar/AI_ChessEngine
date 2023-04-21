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

# testing out monte carlo with depth of one (will expand to depth of two later)
def monte_carlo(model_path, board, turn):
    legal_moves = list(board.get_legal_moves())
    original_FEN = board.get_fen()
    model = tf.keras.models.load_model(model_path)

    if turn == "white":
        best1 = white_monte(legal_moves, original_FEN, model)
    else:
        best1 = black_monte(legal_moves, original_FEN, model)

    return best1

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

    return curr_best_move

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

    return curr_best_move

if __name__ == '__main__':
    board = ChessBoard()
    model_path = '../models/keon/saved_models/model_example.h5'
    # example_use_of_model(model_path, board)
    board.make_move("g1h3")
    board.make_move("g8h6")
    print(monte_carlo(model_path, board, "white"))
    # test_moves()
