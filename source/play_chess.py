"""
This script will be the one that plays chess by using Monte Carlo + our trained Neural Network. 
This simply connects as a wrapper between our board script, our model, and our Monte Carlo 
implementation.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Imports
import sys
import os

import tensorflow as tf
import numpy as np

# Local Imports
from new_board import ChessBoard

def find_best_move(model, board, turn):
    """
    This function finds the best move predicted by a model by looking at all of the 
    possible moves and chooisng the one that the model predicts yields the best position.

    Args:
        model: The trained Tensorflow's Keras model
        board: A PyChess board
        turn: Either 'white' or 'black'
    """
    # Get the starting FEN to return back
    starting_fen = board.get_fen()

    legal_moves = list(board.get_legal_moves())

    # print([str(i) for i in legal_moves])

    # Iterate over potential moves and save predictions
    move_predictions = []
    for potential_move in legal_moves:
        board.make_move(str(potential_move))

        # Check if it is checkmate
        if board.is_in_checkmate():
            board.set_fen(starting_fen)
            return potential_move

        # Predict the stockfish evaluation of the board after move is made
        this_board_encoding = board.positional_encode()
        this_prediction = model.predict(np.array([this_board_encoding]), verbose=0)
        move_predictions.append(this_prediction)

        # Reset board so we have a fresh board for next iteration
        board.set_fen(starting_fen)

    # print(move_predictions)

    # Sanity check
    assert len(move_predictions) == len(legal_moves)

    # Return the best move based on who's turn it is 
    if turn == 'white':
        return legal_moves[np.argmax(move_predictions)]

    if turn == 'black':
        return legal_moves[np.argmin(move_predictions)]

def play_game(board, model1, model2):
    """
    This will be the main thing that plays games!
    """
    turn = 'white'

    while not (board.game_is_done())[0]:
        print('\n------\n')
        print(f'board fen: {board.get_fen()}')
        board.print_board()
        print(f'End status: {(board.game_is_done())[0]}')
        print('\n------\n')
        
        model_to_move = model1 if turn == 'white' else model2
        best_move_prediction = find_best_move(model_to_move, board, turn)
        print(f'move pred: {str(best_move_prediction)}')

        # Make best move predicted by the model
        board.make_move(str(best_move_prediction))
        print(f"{turn}'s made the move - {str(best_move_prediction)}")

        # Update turn
        turn = 'white' if turn == 'black' else 'black'

    



    



def main():
    MODEL1_PATH = '../models/corey/saved_models/model7.h5'
    model1 = tf.keras.models.load_model(MODEL1_PATH)

    MODEL2_PATH = '../models/corey/saved_movels/model0.h5'
    model2 = tf.keras.models.load_model(MODEL1_PATH) 

    board = ChessBoard()
    
    play_game(board, model1, model2)

if __name__ == '__main__':
    main()
