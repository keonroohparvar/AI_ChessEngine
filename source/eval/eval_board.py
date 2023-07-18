"""
This script will serve as the master function used to evaluate a board, and it will tie in all of 
the other scrips that have been generated for board evaluation. It implements the `evaluate_board` 
function that will take in a board object and return the best move for White or Black.
"""

# Importss
import os
import sys
import time

import tensorflow as tf
import numpy as np

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from board import ChessBoard
from eval.alpha_beta import ab_pruning

def evaluate_board(board: ChessBoard, model: tf.keras.Model, turn: str, print_boards: bool = False):
    """
    The high-level function that is able to take in a board and find the best move for White or Black. 

    Arguments:
        board (ChessBoard): Our board object
        model (tf.keras.Model): The model object who is responsible for this turn
        turn (str): Either 'W' or 'B' for white or black, respectively 
        print_board (bool): A tool for debugging, it prints the intermediate boards and their guessed evals
    """
    
    # Time logging for eval board
    start_time = time.time()

    # Save other person's turn
    other_turn = 'B' if turn == 'W' else 'W'

    # Get Possible moves
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    # legal_moves = [list(board.get_legal_moves())[11]]
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)
    
    # Perform Alpha Beta Pruning on all of the possible boards
    possible_board_values = []
    depths = []
    for idx, possible_board in enumerate(possible_boards):
        game_is_done, reason = possible_board.game_is_done()
        if game_is_done:
            if reason == 'checkmate':
                return str(legal_moves[idx]), (np.inf if turn == 'W' else (-1*np.inf))
        _, this_val, depth_reached = ab_pruning(other_turn, possible_board, max_depth=3)
        possible_board_values.append(this_val)
        depths.append(depth_reached)

    # Go over maximum boards and evaluate with model
    contains_checkmate = False
    if turn == 'W':
        boards_to_eval = [(i,move, depth) for (i,j, move, depth) in zip(possible_boards, possible_board_values, legal_moves, depths) if j == np.max(possible_board_values)]
        if np.inf in possible_board_values:
            contains_checkmate = True
    if turn == 'B':
        boards_to_eval = [(i,move, depth) for (i,j,move, depth) in zip(possible_boards, possible_board_values, legal_moves, depths) if j == np.min(possible_board_values)]
        if -1 * np.inf in possible_board_values:
            contains_checkmate = True

        

    if print_boards:
        print('\n---FINAL PRINT BOARDS----')
        for board,val,depth in zip(possible_boards, possible_board_values, depths):
            board.print_board()
            print(f'ab pruning val: {val} - depth: {depth}\n\n')


    # If there is a checkmate possible, we choose the board with the min depth reached
    if contains_checkmate:
        # Sort boards to eval by their depths reached (we want the one that went the minimum depth)
        boards_to_eval.sort(key=lambda x: x[2])
        if turn == 'W':
            return str(boards_to_eval[0][1]), np.inf
        if turn == 'B':
            return str(boards_to_eval[0][1]), -1 * np.inf

    if len(boards_to_eval) == 1:
        if turn == 'W':
            return str(boards_to_eval[0][1]), np.max(possible_board_values)
        if turn == 'B':
            return str(boards_to_eval[0][1]), np.min(possible_board_values)

    preds = [model.predict(np.array([i[0].positional_encode()]), verbose=0)[0][0] for i in boards_to_eval]


    if turn == 'W':
        best_pred_ind = np.argmax(preds)
        return str(boards_to_eval[best_pred_ind][1]), np.max(preds) 
    
    if turn == 'B':
        best_pred_ind = np.argmin(preds)
        return str(boards_to_eval[best_pred_ind][1]), np.min(preds) 
        