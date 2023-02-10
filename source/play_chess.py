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
import chess

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
    starting_fen = board.get_fen()

    legal_moves = board.get_


def play_game():
    """
    This will 
    """
    pass

