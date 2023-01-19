"""
This script will be where we train the model off of Lichess positions so that it learns how to
approximate Stockfish's evaluation for a certain position. 

Incrementally, this script will save models to the saved_models/ directory, so that we will have 
model examples of how it looks through training.

Author: Keon Roohparvar
Date: 11/3/2022
"""

# Python Imports
import os
import argparse
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# Local Imports
from model_architecture import ChessAIModel

def strlist_to_list(l):
    """
    This function will take a string representation of a list and convert it into a python list.
    For example, it will take the string representation '[1, 2, 3]' -> List([1, 2, 3])

    Arguments: 
        l (String): the string representation of a list
    Output:
        List: the list object
    """
    l_split = l.strip('][').split(', ')
    l_ints = [int(i) for i in l_split]
    return l_ints

def load_dataset(filepath):
    """
    This will simply load in the data we have already processed in data_handler.py, but it will
    be used in this file

    Arguments:
        filepath (str): Location of our .csv file
    
    Output:
        array: Array of data points we will use
    """
    df = pd.read_csv(filepath, header=None)

    # Bound values between [-15, 15]
    y = df.pop(df.columns[-1])
    y = y.clip(upper=15, lower=-15)
    print(y.head())

    # Split into training + testing
    train_x, test_x, train_y, test_y = train_test_split(df, y, test_size=0.2)

    return train_x, test_x, train_y, test_y

def get_model(type_of_model, learning_rate):
    """
    This will interface with the model_architecture file to retrieve the proper model we want to 
    use for training.

    Argument:
        type_of_model (str): The type of model we want to retreive. Currently only 'simple' is supported.
    
    Output:
        keras model: A keras model instance
    """
    # Create model class
    model = ChessAIModel(learning_rate)
    return model.get_model(type_of_model)


def train_model(training_csv):
    """
    This is the big function that will train our neural network. 

    Argument:
        training_csv (filepath): The location of where our trainng fata is that we preprocessed
        in our data_handler.py file.
    """
    # HYPERPARAMETERS
    MODEL_TYPE = 'simple'
    NUM_EPOCHS = 100
    BATCH_SIZE = 128
    LEARNING_RATE = 1e-3

    # Load in data
    train_x, test_x, train_y, test_y = load_dataset(training_csv)

    # Retrieve model
    model = get_model(MODEL_TYPE, LEARNING_RATE)

    # Train Model
    model.fit(
        x=train_x, 
        y=train_y,
        epochs=NUM_EPOCHS,
        batch_size=BATCH_SIZE,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_location', type=str)

    args = parser.parse_args()

    if not args.csv_location or (not os.path.isfile(args.csv_location)):
        print('ERROR - Did not provide a correct location to the training .csv file.')
        exit(-1)

    train_model(args.csv_location)