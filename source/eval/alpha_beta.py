"""
This script will be the Monte Carlo implementation that will be the way our Chess Engine is able
to go down potential moves and choose the best one.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Imports
import os
import sys
import time

import tensorflow as tf
import numpy as np

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from board import ChessBoard
from eval.count_material import eval_material


def alphaBetaMax(board, alpha, beta, depth, max_depth):
    print(f'in max, depth is {depth} and board is ->')
    board.print_board()
    print(f'fen is {board.get_fen()}')
    print(f'ev is : {eval_material(board)}')
    # If Depth is max depth, we are at the end and we'll return the evaluation of this board
    if depth == max_depth:
        # this_evaluation = model.predict(np.array([board.positional_encode()]), verbose=0)[0][0]
        this_evaluation = eval_material(board)
        return this_evaluation

    
    print(f'IN MAX, LOOKING FOR Max MOVES.....')
    # Get Possible moves
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)
    
    # Iterate over moves while updating alpha; also, we watch for a beta break
    for board in possible_boards:
        this_board_score = alphaBetaMin(board, alpha, beta, depth+1, max_depth)
        if this_board_score >= beta:
            print(f'beta cutoff of {beta} as this board score is {this_board_score}')
            return beta
        if this_board_score > alpha:
            alpha = this_board_score
    print(f'Exiting max with alpha of {alpha}') 
    return alpha


def alphaBetaMin(board, alpha, beta, depth, max_depth):
    print(f'in min, depth is {depth} and board is ->')
    board.print_board()
    print(f'fen is {board.get_fen()}')
    print(f'ev is : {eval_material(board)}')
    # If Depth is max depth, we are at the end and we'll return the evaluation of this board
    if depth == max_depth:
        # this_evaluation = model.predict(np.array([board.positional_encode()]), verbose=0)[0][0]
        this_evaluation = eval_material(board)
        return this_evaluation

    print('In min looking for Min Boards....')

    # Get Possible moves
    starter_board_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(starter_board_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)
    
    # Iterate over moves while updating beta; also, we watch for an alpha break
    for board in possible_boards:
        this_board_score = alphaBetaMax(board, alpha, beta, depth+1, max_depth)
        if this_board_score <= alpha:
            # print('cutoff!')
            print(f'ALpha cutoff of {alpha} with board score of {this_board_score}')
            return alpha
        if this_board_score < beta:
            beta = this_board_score
    
    print(f'returning from min with beta of {beta}')
    return beta

def ab_pruning(turn, board, max_depth):
    print(f'\n----ROOT-----\nTurn is {turn}, board is ->')
    board.print_board()
    print(f'fen is {board.get_fen()}')
    ev = eval_material(board)
    print(f'ev is : {ev}')
    print('\n--\n')
    # Get all possible boards from this point
    original_fen = board.get_fen()
    legal_moves = list(board.get_legal_moves())
    possible_boards = []
    for legal_move in legal_moves:
        new_board = ChessBoard()
        new_board.set_fen(original_fen)
        new_board.make_move(str(legal_move))
        possible_boards.append(new_board)

    # Go through possibilities and do alpha beta pruning
    values = []
    times = []
    for board in possible_boards:
        starttime = time.time()
        if turn == 'W':
            this_value = alphaBetaMin(board, alpha=-1*np.inf, beta=np.inf, depth=1, max_depth=max_depth)
        elif turn == 'B':
            this_value = alphaBetaMax(board, alpha=-1*np.inf, beta=np.inf, depth=1, max_depth=max_depth)

        endtime = time.time()
        times.append(endtime - starttime)

        # print(f'this val: {this_value}')
        values.append(this_value)
    
    print('--RETURNED TO ROOT--')
    print(f'Vals: {values}')


    # Choose the board that yields the highest value
    if turn == 'W':
        best_move = legal_moves[np.argmax(values)]
        print(f'Best move: {best_move}\n----\n')
        return best_move, np.max(values)
    else:
        best_move = legal_moves[np.argmin(values)]
        print(f'Best move: {best_move}\n----\n')
        return best_move, np.min(values)
    
    
def find_best_move_ab_pruning(board, turn):
    """
    This function finds the best move predicted by a model by looking at all of the 
    possible moves and chooisng the one that the model predicts yields the best position.

    Args:
        board: A PyChess board
        turn: Either 'W' or 'B'
    """
    legal_moves = list(board.get_legal_moves())

    if len(legal_moves) == 0:
        return -1

    best_move = ab_pruning(turn, board, max_depth=4)

    return best_move
