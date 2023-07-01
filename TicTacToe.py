import numpy as np

class TicTacToe():
    def __init__(self,playerOne,playerTow):
        self.playerOne = playerOne
        self.playerTwo = playerTow
        self.currentGame = np.full((3, 3), '-', dtype=str)
        self.currentPlayer = '1'

    def __str__(self):
        returnString = ''
        for row in self.currentGame:
            for item in row:
                returnString += item +' '
            returnString += '\n'
        return returnString

    def makeMove(self, newMove):
        if ((newMove['row'] > 2) | (newMove['col'] > 2)):
            return -2
        elif self.currentGame[newMove['row'],newMove['col']] != "-":
            return -1
        else:
            self.currentGame[newMove['row'],newMove['col']] = self.playerOne if self.currentPlayer== '1'else self.playerTwo
            self.currentPlayer = '2' if self.currentPlayer == '1' else '1'
            return 1

    def checksForWinner(self):
        checksPlayerOne = np.where(self.currentGame == self.playerOne, 1 ,0)
        checksPlayerTwo = np.where(self.currentGame == self.playerTwo, 1 ,0)

        if self.checksPlayer(checksPlayerOne) == 1: return 1
        elif self.checksPlayer(checksPlayerTwo) == 1: return 2
        else: return 0

    def checksPlayer(self, movementsMatrix):
        #Checks for column plays
        sumCols = np.sum(movementsMatrix, axis=0)
        for sum in sumCols:
            if sum == 3: return 1
        #Checks for rows plays
        sumRows = np.sum(movementsMatrix, axis=1)
        for sum in sumRows:
            if sum == 3: return 1
        #Check for diagonal plays
        if (movementsMatrix[0,0] + movementsMatrix[1,1] + movementsMatrix[2,2] == 3): return 1
        if (movementsMatrix[0,2] + movementsMatrix[1, 1] + movementsMatrix[2,0] == 3): return 1

        return 0 #if not winner move return 0