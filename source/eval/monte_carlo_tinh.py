"""
This script implements a Monte Carlo approach for our Chess Engine, enabling it to evaluate potential moves and select the best one.

Author: Tinh-Phong Nguyen
Date: 8/15/2024
"""

# Imports
import os
import sys
import tensorflow as tf
import numpy as np

# Local imports
from board import ChessBoard

def load_model(model_path):
    """Load and return the TensorFlow model."""
    print(f'Loading model from {model_path} ...')
    return tf.keras.models.load_model(model_path)

def evaluate_board(model, board):
    """Evaluate the board using the loaded model."""
    board_encoding = board.positional_encode()
    board_array = np.array([board_encoding])
    prediction = model.predict(board_array, verbose=0)[0][0]
    return prediction

def example_use_of_model(model, board):
    """Demonstrate making a move and using the model to evaluate the board."""
    
    print('Initial board state:')
    board.print_board()
    print('\n-------\n')

    # Get all legal moves
    legal_moves = list(board.get_legal_moves())

    if not legal_moves:
        print("No legal moves available.")
        return

    # Example: making the first legal move
    original_FEN = board.get_fen()
    example_move = legal_moves[0]
    
    print(f'Example move: {example_move}\n')
    
    board.make_move(str(example_move))
    print('Board after making the move:')
    board.print_board()
    print('\n-------\n')

    # Revert board to original state
    board.set_fen(original_FEN)

    # Evaluate the board using the model
    prediction = evaluate_board(model, board)
    print(f'Model evaluation of the board: {prediction}\n-------\n')


if __name__ == '__main__':
    board = ChessBoard()
    model_path = '../models/keon/saved_models/model_example.h5'
    
    # Load model once
    model = load_model(model_path)
    
    # Use the model to evaluate the board
    example_use_of_model(model, board)
