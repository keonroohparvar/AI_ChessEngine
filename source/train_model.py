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


# Local Imports
from model_architecture import ChessAIModel
from data_handler import load_our_dataset

def load_data_from_csv(filepath):
    """
    This will simply load in the data we have already processed in data_handler.py, but it will
    be used in this file

    Arguments:
        filepath (str): Location of our .csv file
    
    Output:
        array: Array of data points we will use
    """
    with open(filepath, 'r') as f:
        return f.readlines()

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
    BATCH_SIZE = 16
    LEARNING_RATE = 0.01

    # Load in data
    X, Y = load_our_dataset(training_csv)

    print(X)
    return

    # Retrieve model
    model = get_model(MODEL_TYPE, LEARNING_RATE)

    # Train Model
    model.fit(
        x=X, 
        y=Y,
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