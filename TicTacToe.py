import numpy as np

class TicTacToe():
    def __init__(self,playerOne,playerTow):
        self.playerOne = playerOne
        self.playerTwo = playerTow
        self.currentGame = np.full((3, 3), '-', dtype=str)
        self.currentPlayer = '1'
        self.moveNumber = 0

    def __str__(self):
        returnString = ''
        for row in self.currentGame:
            for item in row:
                returnString += item +' '
            returnString += '\n'
        return returnString
    def getCurrentPlayer(self):
        return self.currentPlayer

    def addMoveCount(self, add):
        self.moveNumber += add
    def reset(self):
        self.currentGame = np.full((3, 3), '-', dtype=str)
        self.currentPlayer = '1'
        self.moveNumber = 0

    def makeMove(self, newMove):
        if ((newMove['row'] > 2) | (newMove['col'] > 2)):
            return -2
        elif self.currentGame[newMove['row'],newMove['col']] != "-":
            return -1
        else:
            self.currentGame[newMove['row'],newMove['col']] = self.playerOne if self.currentPlayer== '1'else self.playerTwo
            self.currentPlayer = '2' if self.currentPlayer == '1' else '1'
            self.addMoveCount(1)
            return 1

    def checksForWinner(self):
        checksPlayerOne = np.where(self.currentGame == self.playerOne, 1 ,0)
        checksPlayerTwo = np.where(self.currentGame == self.playerTwo, 1 ,0)

        if self.checksPlayer(checksPlayerOne) == 1: return 1
        elif self.checksPlayer(checksPlayerTwo) == 1: return 2
        elif self.checksDraw() == 9: return 3
        else: return 0
    def checksDraw(self):
        counter = 0
        for row in self.currentGame:
            for item in row:
                counter += 1 if item != "-" else 0
        return counter
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
        if ((movementsMatrix[0,0] + movementsMatrix[1,1] + movementsMatrix[2,2]) == 3): return 1
        if ((movementsMatrix[0,2] + movementsMatrix[1, 1] + movementsMatrix[2,0]) == 3): return 1

        return 0 #if not winner move return 0
    def createMove(self):
        #try to create an automate movement
        checksThread = self.possibleWinner(self.playerOne)
        checksAttackWinner = self.possibleWinner(self.playerTwo)
        createAttackMove = self.attackMove()
        #If is the begining of game and center is available is taken for the machine
        if (self.moveNumber == 1 and self.currentGame[1,1] == '-'):
            self.makeMove({'row':1,'col':1})
        elif (self.moveNumber == 1 and self.currentGame[1,1] == self.playerOne): #opponent opens at center, then a corner is played
            self.makeMove({'row':0, 'col':2})
        elif(checksAttackWinner['status']):
            #Atacks if there is the change to complete 3 in a row
            self.makeMove(checksAttackWinner['move'])
        elif(checksThread['status']):
            # Adopts a defensive position if there are two taken places by adversary
            self.makeMove(checksThread['move'])
        elif(createAttackMove['status']):
            self.makeMove(createAttackMove['move'])
        else:
            self.makeMove(self.randomChoose()) #other case choose a random available position
    def randomChoose(self):
        for i in range(self.currentGame.shape[0]):
            for j in range(self.currentGame[i,:].shape[0]):
                if self.currentGame[i,j] == "-":
                    return {'row':i,'col':j}

    def attackMove(self):
        currentGameCopy = self.currentGame.copy()
        for i in range(self.currentGame.shape[0]):
            for j in range(self.currentGame[i,:].shape[0]):
                if self.currentGame[i,j] == "-":
                    self.currentGame[i, j] = self.playerTwo
                    checksWinnerPlay = self.possibleWinner(self.playerTwo)
                    if (checksWinnerPlay['status']):
                        self.currentGame = currentGameCopy
                        return checksWinnerPlay
                    else:
                        self.currentGame[i, j] = "-"
        return {'status':False}

    def possibleWinner(self, player):
        #if the user has 2 movements, this procedure retreives true and the required direction to block the winner
        checksPlayer = np.where(self.currentGame == player, 1, 0)
        #columns checks
        columnCheck = self.checksThread(checksPlayer,0)
        if columnCheck['status']:
            return columnCheck
        #rows checks
        rowCheck = self.checksThread(checksPlayer,1)
        if rowCheck['status']:
            return rowCheck
        #diags checks
        if ((checksPlayer[0, 0] + checksPlayer[1, 1] + checksPlayer[2, 2]) == 2):
            if self.currentGame[0, 0] == "-":
                return {'status': True, 'move': {"row": 0, "col": 0}}
            elif self.currentGame[1, 1] == "-":
                return {'status': True, 'move': {"row": 1, "col": 1}}
            elif self.currentGame[2, 2] == "-":
                return {'status': True, 'move': {"row": 2, "col": 2}}

        if ((checksPlayer[2, 0] + checksPlayer[1, 1] + checksPlayer[0, 2]) == 2):
            if self.currentGame[2, 0] == "-":
                return {'status': True, 'move': {"row": 0, "col": 0}}
            elif self.currentGame[1, 1] == "-":
                return {'status': True, 'move': {"row": 1, "col": 1}}
            elif self.currentGame[0, 2] == "-":
                return {'status': True, 'move': {"row": 0, "col": 2}}

        return {'status':False}
    def checksThread(self,arrayCheck, axisValidate):

        sumDim = np.sum(arrayCheck, axis=axisValidate)
        for i in range(sumDim.shape[0]):
            if sumDim[i] == 2:
                dimToCheck = self.currentGame[:, i] if axisValidate == 0 else self.currentGame[i, :]
                notAlreadyPlayed = sum(np.where(dimToCheck == '-', 1, 0))  # if there is not "-" in the dimension continues
                if notAlreadyPlayed != 0:
                    for j in range(dimToCheck.shape[0]):
                        if dimToCheck[j] == '-':
                            if axisValidate == 0:
                                return {'status': True, 'move': {"row": j, "col": i}}
                            else:
                                return {'status': True, 'move': {"row": i, "col": j}}
                            break
        return{'status':False}