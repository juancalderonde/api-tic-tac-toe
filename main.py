from flask import Flask, jsonify, request
from TicTacToe import TicTacToe
import json

app = Flask(__name__)
game = TicTacToe('X', 'O')


@app.route("/api/newGame", methods=['GET'])
def playTicTacToe():
    game = TicTacToe('X', 'O')
    return game.__str__()

@app.route("/api/makeMove", methods=['POST'])
def makeMove():
    movement = request.json
    result = game.makeMove(movement)
    if result == -1:
        return jsonify({'error':'Already position taken'}), 400
    elif result == -2:
        return jsonify({'error':'Posicion Out of bound'}), 400
    else:
        return game.__str__()

@app.route("/api/checksWinner", methods=['GET'])
def checksWinner():
    winner = game.checksForWinner()
    if winner == 1: return jsonify({'ganador':'Player 1'})
    elif winner == 2: return jsonify({'ganador':'Player 2'})
    else: return jsonify({'ganador':'Aun nadie ha ganado'})

if __name__=='__main__':
    app.run(port=8082)