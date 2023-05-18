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
from board import ChessBoard


def alphaBetaMax(board, model, alpha, beta, depth, max_depth):
    # If Depth is max depth, we are at the end and we'll return the evaluation of this board
    if depth == max_depth:
        this_evaluation = model.predict(np.array([board.positional_encode()]), verbose=0)[0][0]
        return this_evaluation

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
        this_board_score = alphaBetaMin(board, model, alpha, beta, depth+1, max_depth)
        if this_board_score >= beta:
            # print('cutoff!')
            return beta
        if this_board_score > alpha:
            alpha = this_board_score
    
    return alpha



def alphaBetaMin(board, model, alpha, beta, depth, max_depth):
    # If Depth is max depth, we are at the end and we'll return the evaluation of this board
    if depth == max_depth:
        this_evaluation = model.predict(np.array([board.positional_encode()]), verbose=0)[0][0]
        return this_evaluation

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
        this_board_score = alphaBetaMax(board, model, alpha, beta, depth+1, max_depth)
        if this_board_score <= alpha:
            # print('cutoff!')
            return alpha
        if this_board_score < beta:
            beta = this_board_score
    
    return beta

def ab_pruning(turn, board, model, max_depth):
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
            this_value = alphaBetaMax(board, model, alpha=-1*np.inf, beta=np.inf, depth=1, max_depth=max_depth)
        elif turn == 'B':
            this_value = alphaBetaMin(board, model, alpha=-1*np.inf, beta=np.inf, depth=1, max_depth=max_depth)

        endtime = time.time()
        times.append(endtime - starttime)

        # print(f'this val: {this_value}')
        values.append(this_value)

    # Choose the board that yields the highest value
    if turn == 'W':
        best_move = legal_moves[np.argmax(values)]
    else:
        best_move = legal_moves[np.argmin(values)]
    
    print(f'Mean AB time: {np.mean(times)}')
    
    return best_move

def find_best_move_ab_pruning(model, board, turn):
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

    best_move = ab_pruning(turn, board, model, max_depth=2)

    return best_move

if __name__ == '__main__':
    board = ChessBoard()
    model_path = '../models/keon/saved_models/model_example.h5'
    # example_use_of_model(model_path, board)
    
