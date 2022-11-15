"""
This script will pull data from Lichess, and save it in the data/ folder for us to train our 
model on. 

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Keon
def pull_only_stockfish_games(in_filepath, out_filepath):
    """
    This will parse the downloaded file and get the game strings from it.
    """
    with open(out_filepath, 'w') as fw:
        with open(in_filepath, 'r') as fr:
            for line in fr:
                if line[0] == '1' and ('eval' in line):
                    fw.write(line)

# Keon
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
    result = []
    game_string = game_string.split("...")
    game_string[0] = game_string[0][2:]
    for i in range(len(game_string)):
        game_string[i] = game_string[i][1:]
        game_string[i] = game_string[i].split(" ")
    for i in range(len(game_string)):
        if (i == 0 or i == (len(game_string) - 1)) and game_string[i][3][0] == "#":
            result.append((game_string[i][0], game_string[i][3][:-1]))
        elif (i == 0 or i == (len(game_string) - 1)) and game_string[i][3][0] != "#":
            result.append((game_string[i][0], float(game_string[i][3][:-1])))
        elif game_string[i][3][0] == "#" and game_string[i][3][0]:
            result.append((game_string[i][0], game_string[i][3][:-1]))
            result.append((game_string[i][6], game_string[i][9][:-1]))
        elif game_string[i][9][0] == "#":
            result.append((game_string[i][0], float(game_string[i][3][:-1])))
            result.append((game_string[i][6], game_string[i][9][:-1]))
        elif game_string[i][3][0] == "#":
            result.append((game_string[i][0], game_string[i][3][:-1]))
            result.append((game_string[i][6], float(game_string[i][9][:-1])))
        else:
            result.append((game_string[i][0], float(game_string[i][3][:-1])))
            result.append((game_string[i][6], float(game_string[i][9][:-1])))
    return result


# Jeremy
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

# Devon
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

if __name__ == '__main__':
    # Get All Games
    games = pull_all_games('small_game_dataset.txt')

    print(f"Here is an example game: \n{games[0]}")


    file = open('small_game_dataset.txt', "r")
    lines = file.readlines()
    print(parse_game_string_to_list(lines[0]))

    

