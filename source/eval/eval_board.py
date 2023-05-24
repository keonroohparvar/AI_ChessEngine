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
from eval.count_material import eval_material
from alpha_beta import ab_pruning

def evaluate_board(board: ChessBoard, model: tf.keras.Model, turn: str, print_boards: bool = False):
    # Save other person's turn
    other_turn = 'B' if turn == 'W' else 'W'

    # Get Possible moves
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    # legal_moves = [list(board.get_legal_moves())[1]]
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)

    # Perform Alpha Beta Pruning on all of the possible boards
    possible_board_values = []
    for possible_board in possible_boards:
        _, this_val = ab_pruning(other_turn, possible_board, max_depth=2)
        possible_board_values.append(this_val)

    # Go over maximum boards and evaluate with model
    if turn == 'W':
        boards_to_eval = [(i,move) for (i,j, move) in zip(possible_boards, possible_board_values, legal_moves) if j == np.max(possible_board_values)]
    if turn == 'B':
        boards_to_eval = [(i,move) for (i,j,move) in zip(possible_boards, possible_board_values, legal_moves) if j == np.min(possible_board_values)]


    if print_boards:
        print('\n---FINAL PRINT BOARDS----')
        for board,val in zip(possible_boards, possible_board_values):
            board.print_board()
            print(f'ab pruning val: {val}\n\n')

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
        
if __name__ == '__main__':
    board = ChessBoard()
    # model = tf.keras.models.load_model('../../models/keon/saved_models/model_example.h5')
    model = tf.keras.models.load_model('/Users/keonroohparvar/Dev/SPD_Chessbot/models/keon/saved_models/model_example.h5')
    # best_move = evaluate_board(board, model, 'W', True)
    # print(f'best move: {best_move}')

    # fen = '5kr1/5p1p/5PRP/6P1/8/8/8/7K w - - 0 1'
    fen = '5kr1/5p1p/5PRP/4N1P1/8/8/8/7K w - - 0 1'
    while fen.lower() != 'quit' or fen.lower() != 'q':
        # fen = input("fen: ")
        board.set_fen(fen)
        # board.print_board()
        # ev = eval_material(board)
        # print(f'material: {ev}')

        turn = 'W' if board.get_turn() else 'B'
        print(f'board get turn: {board.get_turn()}')
        print(f'turn is {turn}')
        best_move, eval = evaluate_board(board, model, turn, True)
        print(f'best move: {best_move}')

        exit()

