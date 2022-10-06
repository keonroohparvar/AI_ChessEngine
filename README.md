# SPD_Chessbot

This repository contains all of the implementation for the SPD Chess AI model. 

## Folder Structure

The folder structure is described below:

```
.
├── README.md                   # This file
├── RL_model                    # Folder that contains AI development
│   ├── model_architecture.py   # The implemenetation of our model
│   ├── saved_models            # Folder that contains different versions of our AI
│   └── train_model.py          # The file that has our model play against itself
├── board.py                    # The Chess board implementation
└── requirements.txt            # File detailing how to get setup
```

## Setup

The process for getting this code setup is by following the steps below (please hit me up if you have questions):

1. Ensure you have python installed. If you are not sure, type `$ python3 -V` in your terminal.
2. Clone this repository somewhere locally on your computer.
3. Create a python environment using `$ python3 -m venv venv` - this should create a folder named `venv/` in your directory
4. Activate this virtual environment by running `$ source venv/bin/activate`
5. Install all packages by running `pip install tensorflow` (I think this is it lol, but this might break idk we'll find out)

That's it! To check this all works, type `python` into the terminal and type `import tensorflow` to ensure that you properly installed the packages. If you did, congrats! You are done with setup.

