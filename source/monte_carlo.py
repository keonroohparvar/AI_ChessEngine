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

def mc_eval_board(turn, board, current_depth, max_depth):
    """
    this is the recursive function that will eval a board.
    NOTE: this probably doesn't work but this is close i think hahah i did not test this sorry my kings

    # Function for switching turns
    def switch_turn(turn):
        if turn == 'W':
            return 'B'
        else:
            return 'W'

    # Get current evaluation
    curr_eval = evaluation of the "board" parameter
    
    

    # CHECK IF WE ARE AT MAX DEPTH - IF WE DONT DO THIS, WE RECURSE FOREVER
    if max_depth == current_depth:
        return evaluation of our current board
    
    # Get all possible boards
    possible_boards = all possible boards from this board
    
    # Handle cases differently for both teams ->

    # If turn is W, we will return the max of the options (because white wants to maximize)
    if turn == 'W':
        other_turn = 'B'
        return curr_eval + max([mc_eval_board(other_turn, i, current_depth + 1, max_depth) for i in possible_boards])
    
    # If turn is B, we will return the min of the options (because black wants to minimize)
    if turn == 'B':
        other_turn = 'W'
        return curr_eval + min([mc_eval_board(other_turn, i, current_depth + 1, max_depth) for i in possible_boards])
        
    """
    pass

def monte_carlo(board, max_depth):
    """
    turn = 'W' (if we are white, 'B' else)

    # GO thru all the boards
    possible_boards = all possible boards that we can move to

    # GO through possibilities and do MCTS
    values = []
    for board in possible_boards:
        this_value = mc_eval_board(board, current_depth=0, max_depth=max_depth)
        values.append(this_value)

    # Choose the board that yields the highest value
    best_board = max(values)
    """
    pass


if __name__ == '__main__':
    board = ChessBoard()
    model_path = '../models/keon/saved_models/model_example.h5'
    example_use_of_model(model_path, board)
    
