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
import argparse

import tensorflow as tf
import numpy as np

# Local Imports
from board import ChessBoard
from eval.minimax import find_best_move_minimax
from eval.alpha_beta import find_best_move_ab_pruning

def find_best_move(model, board, turn):
    """
    This function finds the best move predicted by a model by looking at all of the 
    possible moves and chooisng the one that the model predicts yields the best position.

    Args:
        model: The trained Tensorflow's Keras model
        board: A PyChess board
        turn: Either 'W' or 'B'
    """
    # Get the starting FEN to return back
    starting_fen = board.get_fen()

    legal_moves = list(board.get_legal_moves())

    if len(legal_moves) == 0:
        return -1

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

        this_prediction = model.predict(np.array([this_board_encoding]), verbose=0)[0][0]
        # print(f'pred: {this_prediction}')
        move_predictions.append(this_prediction)

        # Reset board so we have a fresh board for next iteration
        board.set_fen(starting_fen)

    # print(move_predictions)

    # Sanity check
    assert len(move_predictions) == len(legal_moves)

    # Return the best move based on who's turn it is 
    if turn == 'W':
        return legal_moves[np.argmax(move_predictions)]

    if turn == 'B':
        return legal_moves[np.argmin(move_predictions)]

def play_game(board, model1, model2, print_board):
    """
    This will be the main thing that plays games!
    """
    turn = 'W'

    # Keep track of move list
    move_list = []

    while not (board.game_is_done())[0]:
        if print_board:
            print('\n------\n')
            print(f'board fen: {board.get_fen()}')
            board.print_board()
            print('\n------\n')
        
        model_to_move = model1 if turn == 'W' else model2

        ALGORITHMS = ['none', 'minimax', 'ab_pruning']
        CHOSEN_ALGORITHM_INDEX = 2
        CHOSEN_ALGORITHM = ALGORITHMS[CHOSEN_ALGORITHM_INDEX]

        if CHOSEN_ALGORITHM == 'ab_pruning':
            best_move_prediction = find_best_move_ab_pruning(model_to_move, board, turn)
        elif CHOSEN_ALGORITHM == 'minimax':
            best_move_prediction = find_best_move_minimax(model_to_move, board, turn)
        elif CHOSEN_ALGORITHM == 'none': 
            best_move_prediction = find_best_move(model_to_move, board, turn)

        if best_move_prediction == -1:
            print('best move prediction failed :(')
            break
        move_list.append(str(best_move_prediction))

        # Make best move predicted by the model
        board.make_move(str(best_move_prediction))
        print(f"{turn}'s made the move - {str(best_move_prediction)}")

        # Update turn
        turn = 'W' if turn == 'B' else 'B'

    if board.game_is_done()[1] == 'draw':
        print('Draw.')
        return None, move_list

    winning_color = 'W' if turn == 'B' else 'B'
    print(f'{winning_color.upper()} has won the game.')

    return winning_color, move_list

def main(model1_path, model2_path, print_board):
    model1 = tf.keras.models.load_model(model1_path)
    model2 = tf.keras.models.load_model(model2_path) 

    board = ChessBoard()
    
    play_game(board, model1, model2, print_board)

if __name__ == '__main__':
    model1 = '../models/keon/saved_models/model_example.h5'
    model2 = '../models/keon/saved_models/model_example.h5'
    main(model1, model2, True)


"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model1', type=str, help='Path to the model that will play as W.', default=None)
    parser.add_argument('model2', type=str, help='Path to the model that will play as B.', default=None)
    parser.add_argument('--print_board', type=bool, default=True)

    args = parser.parse_args()

    # For hard coding model paths for testing
    HARD_CODE_MODELS = False
    if HARD_CODE_MODELS:
        args.model1 = '../models/keon/saved_models/model_example.h5'
        args.model2 = '../models/keon/saved_models/model_example.h5'

    if not args.model1 or (not os.path.isfile(args.model1)):
        print('ERROR - Did not provide a correct location to the the first model.')
        exit(-1)

    if not args.model2 or (not os.path.isfile(args.model2)):
        print('ERROR - Did not provide a correct location to the the second model.')
        exit(-1)

    main(args.model1, args.model2, args.print_board)
"""