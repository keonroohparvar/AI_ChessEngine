# SPD_Chessbot

This repository contains all of the implementation for the SPD Chess AI model. This is a Chess Engine that I (Keon Roohparvar) led the implementation on for Sigma Phi Delta, the engineering fraternity at Cal Poly SLO. 

The majority of team members were new to programming, so this project was a learning opportunity to give new programmers a change to start interfacing with a fun, difficult project!


## Table of Contents
1. [Folder Structure](#folder-structure)
2. [Setup](#setup)
3. [How It Works](#how-it-works)


## Folder Structure

The folder structure is... 

```
.
├── data                  # Sample data examples of games
├── legacy                # Old code that we don't use anymore
├── models                # Different people's implementations of Neural Networks
└── source
    ├── board.py          # Our implementation of a board
    ├── data_handler.py   # This handles all the interactions with the data
    ├── eval/             # Folder that contains code for evaluating boards (AB pruning, minimax, etc.)
    ├── find_move.py      # High level script that takes a board FEN and finds a move
    ├── play_chess.py     # This has two hard-coded models play against eachother and prints board
    ├── train_model.py    # This trains models on the data
    └── ui                # folder that contains some work on implementing GUI
```


## Setup

The process for getting this code setup is by following the steps below (please hit me up if you have questions):

1. Ensure you have python installed. If you are not sure, type `$ python3 -V` in your terminal.
2. Clone this repository somewhere locally on your computer.
3. Create a python environment using `$ python3 -m venv venv` - this should create a folder named `venv/` in your directory
4. Activate this virtual environment by running `$ source venv/bin/activate`
5. Install tensorflow - This may be challenging, but this [Tensorflow installation Link](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwi3kNPAiN_9AhUsh-4BHfAmCRQQFnoECBYQAQ&url=https%3A%2F%2Fwww.tensorflow.org%2Finstall&usg=AOvVaw1PWhyQVPQQhNfWl2-E7ztd) should help.
6. Install packages in requirements.txt by running `$ pip install -r requirements.txt`

That's it! To check this all works, type `python` into the terminal and type `import tensorflow` to ensure that you properly installed tensorflow properly. If you did, congrats! You are (probably) done, attempt running any of the scripts to ensure that you have the installations correct.


## How it Works

We ultimately employ Alpha-Beta pruning in tandem with Neural networks to evaluate a position.

We use AB pruning to navegate the search tree and immediately eliminate any moves that result in us losing material at a depth of 4 moves into the future.

We then handle ties by having a neural netowkr that was trained on Stockfish evaluations predict over the boards that are tied in us gaining the most material, and the best prediction from the neural network is ultimately the move that we choose.

Currently, the model takes anywhere from 5 seconds to 180 seconds to make a move, so we need to make a lot of work in trying to decrease the time required for moves.
