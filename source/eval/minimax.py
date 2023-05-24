"""
This script will be the Monte Carlo implementation that will be the way our Chess Engine is able
to go down potential moves and choose the best one.

Author: Keon Roohparvar
Date: 11/3/2022
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

def mm_eval_board(turn, board, model, current_depth, max_depth):
    """
    This is the recursive function that will evaluate a board.
    """
    this_evaluation = model.predict(np.array([board.positional_encode()]), verbose=0)[0][0]
    # print(f'This eval: {this_evaluation}')

    # Check if we are at the bottom - then, we are done
    if current_depth >= max_depth:
        return this_evaluation

    # Get all possible boards from this point
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)

    # Handle cases for either White or Black
    if turn == "W":
        other_turn = "B"
        return this_evaluation + min([mm_eval_board(other_turn, sub_board, model, current_depth+1, max_depth) for sub_board in possible_boards])

    if turn == "B":
        other_turn = "W"
        return this_evaluation + max([mm_eval_board(other_turn, sub_board, model, current_depth+1, max_depth) for sub_board in possible_boards])


def minimax(turn, board, model, max_depth):
    # Get all possible boards from this point
    original_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(original_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)

    # Go through possibilities and do MCTS
    values = []
    # print(f'number of boards: {len(possible_boards)}')
    for board in possible_boards:
        this_value = mm_eval_board(turn, board, model, current_depth=1, max_depth=max_depth)
        # print(f'this val: {this_value}')
        values.append(this_value)

    # Choose the board that yields the highest value
    if turn == 'W':
        best_move = legal_moves[np.argmax(values)]
    else:
        best_move = legal_moves[np.argmin(values)]
    
    return best_move

def find_best_move_minimax(model, board, turn):
    """
    This function finds the best move predicted by a model by looking at all of the 
    possible moves and chooisng the one that the model predicts yields the best position.

    Args:
        model: The trained Tensorflow's Keras model
        board: A PyChess board
        turn: Either 'W' or 'B'
    """
    legal_moves = list(board.get_legal_moves())

    if len(legal_moves) == 0:
        return -1

    best_move = minimax(turn, board, model, max_depth=2)

    return best_move

if __name__ == '__main__':
    board = ChessBoard()
    model_path = '../models/keon/saved_models/model_example.h5'
    example_use_of_model(model_path, board)
    
