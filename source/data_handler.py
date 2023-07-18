"""
This script will pull data from Lichess, and save it in the data/ folder for us to train our 
model on. 

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Python imports
from csv import writer
import re
import numpy as np
import pandas as pd

# Local Imports
from board import ChessBoard

def pull_only_stockfish_games(in_filepath, out_filepath):
    """
    This will parse the downloaded file and get the game strings from it.
    """
    with open(out_filepath, 'w') as fw:
        with open(in_filepath, 'r') as fr:
            for line in fr:
                if line[0] == '1' and ('eval' in line):
                    fw.write(line)

def pull_all_games(filepath):
    """
    This function will pull all games from our database of games and return them as an array of strings.
    """
    with open(filepath, 'r') as f:
        return f.readlines()

# Max C.
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
    # print(game_string)
    moves = re.findall(r'\d*\.* (\S*) \{', game_string)
    evals = re.findall(r'\[%eval\s([-A-Za-z0-9_\.\#]+)\]', game_string)

    moves = [i for i in moves if '#' not in i]
    moves = [i.replace('?', '').replace('!', '') for i in moves]

    # They remove evaluations if the move list is longer than 100 moves
    if len(moves) != len(evals):
        # print("ERROR - Moves != evals with game: \n-> ", game_string)
        # print(moves)
        # if len(moves) < 100:
        #     print('\nlength of moves less than 100')
        # print(evals)
        return []

    return list(zip(moves, evals))

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
    board = ChessBoard()
    BoardArrayValues = []

    # Skip first move, and iterate through mvoe list
    for this_move, this_eval in move_list:
        # Push the move
        board.make_move(this_move)
        
        # Get current encoding
        this_encoding = board.positional_encode()

        # Append this encoding and eval to arr
        BoardArrayValues.append((this_encoding, this_eval))
    
    # print(BoardArrayValues)
    return BoardArrayValues

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
    this_game_positional_encodings = convert_game_to_pos_encodings(move_list)
    for board_encoding, stockfish_eval in this_game_positional_encodings:
        with open(data_filepath, 'a') as f:
            f_writer = writer(f)

            if '#' in str(stockfish_eval):
                eval = -100. if '-' in str(stockfish_eval) else 100.
            else:
                eval = float(stockfish_eval)

            f_writer.writerow(board_encoding + [eval])

def data_pipeline(path_to_games_file, num_games=None):
    """
    This is the whole pipeline that our model will call, and this will return a dataframe of our dataset
    """
    games = pull_all_games(path_to_games_file)

    # If num_games is set, choose a random subset of games from that data
    if num_games:
        games_for_training = np.random.choice(games, size=num_games, replace=False)
    else:
        games_for_training = games
    
    # Go over games and do preprocessing
    print('PREPROCESSING THE DATA.....')
    LEN_OF_DATA = 777
    game_dataframe = pd.DataFrame(columns=range(LEN_OF_DATA))
    for game in games_for_training:
        # Turn string into move + eval
        this_move_list = parse_game_string_to_list(game)
        # print('move list: ')
        # print(this_move_list)
    
        if this_move_list != []:

            # Turn move list into positional encoding list
            this_positional_encoding_eval_list = convert_game_to_pos_encodings(this_move_list)
            # print('pos encoding list length: ')
            # print(len(this_positional_encoding_eval_list))
            

            # Append move list to pd dataframe
            for board_encoding, stockfish_eval in this_positional_encoding_eval_list:
                if '#' in str(stockfish_eval):
                    eval = -100. if '-' in str(stockfish_eval) else 100.
                else:
                    eval = float(stockfish_eval)

                row_to_add = pd.Series(board_encoding + [eval])
                game_dataframe = game_dataframe.append(row_to_add)
        
        

def game_to_data(game_str):
    """
    This function will take in a game string and return a batch of data that only corresponds to 
    this specific game.
    """
    # Turn string into move + eval
    this_move_list = parse_game_string_to_list(game_str)

    # Turn move list into positional encoding list
    this_positional_encoding_eval_list = convert_game_to_pos_encodings(this_move_list)

    # Go over games and do preprocessing
    LEN_OF_DATA = 777
    df_cols = range(LEN_OF_DATA)
    game_dataframe = pd.DataFrame(columns=df_cols)

    # Append move list to pd dataframe
    for board_encoding, stockfish_eval in this_positional_encoding_eval_list:
        if '#' in str(stockfish_eval):
            eval = -100. if '-' in str(stockfish_eval) else 100.
        else:
            eval = float(stockfish_eval)

        row_to_add = pd.DataFrame(board_encoding + [eval])
        row_to_add = row_to_add.T
        row_to_add.columns = df_cols
        game_dataframe = pd.concat([game_dataframe, row_to_add], ignore_index=True)
    
    y = game_dataframe.pop(game_dataframe.columns[-1])

    y = y.clip(upper=15, lower=-15)
    y = y / 15

    return game_dataframe, y

        

if __name__ == '__main__':
    data_pipeline('../data/eval_games.txt', 100)
    