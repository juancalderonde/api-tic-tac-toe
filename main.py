from flask import Flask, jsonify, request
from TicTacToe import TicTacToe
import json

app = Flask(__name__)
game = TicTacToe('X', 'O')


@app.route("/api/newGame", methods=['GET'])
def playTicTacToe():
    game.reset()
    #return game.__str__()

@app.route("/api/makeMove", methods=['POST'])
def makeMove():
    movement = request.json
    result = game.makeMove(movement)
    if result == -1:
        return jsonify({'error':'Already position taken'}), 400
    elif result == -2:
        return jsonify({'error':'Posicion Out of bound'}), 400
    else:
        if game.getCurrentPlayer() == '2':
            move = game.createMove()
        return game.__str__()

@app.route("/api/checksWinner", methods=['GET'])
def checksWinner():
    winner = game.checksForWinner()
    if winner == 1: return jsonify({'winner':'Player 1'}), 200
    elif winner == 2: return jsonify({'winner':'Player 2'}), 200
    elif winner == 3: return jsonify({'no_winner':'it´s a draw there is not winner'}), 200
    else: return jsonify({'game':'Still not a winner'}), 200

if __name__=='__main__':
    app.run(port=8082)