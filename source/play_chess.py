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
import time

import tensorflow as tf
import numpy as np

# Local Imports
from board import ChessBoard
from eval.eval_board import evaluate_board

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

        start_time = time.time()
        best_move_prediction, new_eval = evaluate_board(board, model_to_move, turn, False)
        end_time = time.time()
        print(f'Move time: {end_time - start_time}')

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

def main(model1_path, model2_path, starting_fen=None, print_board=False):
    model1 = tf.keras.models.load_model(model1_path)
    model2 = tf.keras.models.load_model(model2_path) 

    board = ChessBoard()

    if starting_fen:
        board.set_fen(starting_fen)
    
    play_game(board, model1, model2, print_board)

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
    