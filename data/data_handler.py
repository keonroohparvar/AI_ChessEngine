"""
This script will pull data from Lichess, and save it in the data/ folder for us to train our 
model on. 

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Keon
def download_games_from_lichess(url):
    """
    This will download games from lichess, save them locally, and format them into a .csv file.
    """
    pass

def parse_game_string_to_list(game_string):
    """
    This converts a game string in the format below to a list of moves.
    Input:
        game_string: String in the format 
            '1. e4 { [%eval 0.17] [%clk 0:00:30] } c5 { [%eval 0.19] [%clk 0:00:30] } ...'
            This string describes the whole game by giving a move number, then White & Black's 
            moves with matching Stockfish evaluation metrics. 
    
    Output:
        list: The list of moves in the format:
            -> [('e4', 0.17), ('c5', 0.19), ...]
    """
    pass

def convert_game_to_pos_encodings(move_list):
    """
    This function will be used to convert our move lists to data we can actually use. It will do 
    this in the following manner:
        1. Create a board object, and an array named BoardArrayValues that will hold our data points
        2. Iterate through the move list. For each move:
            2a) Update our board object with this move
            2b) Convert the board object to a positional encoding
            2c) Save the pair of (positional_encoding, stockfish evaluation) to an array
        3. Return BoardArrayValues
    
    Input:
        move_list (list): List in the following format: 
            [(Move1, Stockfish Eval 1), (Move2, Stockfish Eval 2), ...]
    
    Output:
        BoardArrayValues (list): List in the following format: 
            [(Positional Encoding 1, Stockfish Eval. 1), (Positional Encoding 2, Stockfish Eval. 2), ...]
    """
    pass

def save_move_list_to_csv(move_list, data_filepath):
    """
    This will save the list 'move_list' as a lot of new data points in the csv file located
    at data_filepath. This will use the convert_game_to_pos_encodings() function.

    Inputs:
        move_list (list): List of moves in a single game
        output_filepath (string): The location of our data csv
    
    Output: 
        None
    """
    pass