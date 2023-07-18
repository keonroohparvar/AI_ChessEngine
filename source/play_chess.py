"""
This script will automate a game of chess by using our custom AB-Pruning / Neural Network approach. 
The functionality in this script simply serves as a wrapper between our board script, our model, 
and our AB-Pruning implementation.

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
    The main driver function that simulates games and prints them to Standard Output.

    Arguments:
        board (ChessBoard): a ChessBoard object that will hold our game
        model1 (tf.keras.Model): A Model instance that will play as White
        model2 (tf.keras.Model): A Model instance that will play as Black
        print_board (bool): If we want to print the board to Standard Output

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
    # For hard coding model paths for testing
    model1 = '../models/keon/saved_models/model_example.h5'
    model2 = '../models/keon/saved_models/model_example.h5'

    main(model1, model2,None, True)
    
