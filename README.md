# General Description
This repository creates an api with python using Flask for playing tic-tac-toe, this api allows to create new games and play against a machine.

# Requirements
  - Python 3.9 or above -> https://www.python.org/downloads
  - IDE such as pycharm

# How to build

this api contains a environment with all the libraries necesary to use the program, if needed is possible to run the app as a development server with uncommenting this lines in main.py

  ```bash
    if __name__=='__main__':
      app.run(port=8082)
  ```


# Endpoints 
  /api/newGame: Restart the current game cleaning all moves
  /api/makeMove: Creates a new move by the player, after there is a success move, the machine creates the next move for making the process interactive
  /api/checksWinner: checks if there is a winner, draw or if the game is over without any winner

