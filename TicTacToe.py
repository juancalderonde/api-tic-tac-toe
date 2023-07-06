import numpy as np

class TicTacToe():

    """ Stores all methods to play tic-tac-toe also known as three in a line
    this class allows to perform all the different needed method for the game but so far is only valid to play
    1 vs machine
    """
    def __init__(self,playerOne,playerTow):
        """Constructor Method
        Is only necesary to get the player one and two mark for example P1 -> X P2 -> O

        :param playerOne:       (string) mark use to denote the player1 i.e. "X"
        :param playerTwo:       (string) mark use to denote the player1 i.e. "O"
        :param currentGame:     (numpy Array) stores a 3x3 matrix with the current game, starting only has "-"
        :param currentPlayer:   (string) is the player with the next move to do
        :param moveNumber:      (int) stores the number of plays which has been made

        """
        self.playerOne = playerOne
        self.playerTwo = playerTow
        self.currentGame = np.full((3, 3), '-', dtype=str)
        self.currentPlayer = '1'
        self.moveNumber = 0

    def __str__(self):
        """
        overrides the print statement for this class, it transforms self.currentGame to string 3x3 representation

        :return: String with the representation of the current Game matrix
        """
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
        """
        Method for creating a new empty game

        :return: (void)
        """
        self.currentGame = np.full((3, 3), '-', dtype=str)
        self.currentPlayer = '1'
        self.moveNumber = 0

    def makeMove(self, newMove):
        """
        Stores in self.currentGame a new move to make by self.currentPlayer, if position is already taken returns int with error
        :param newMove: (dict) {"row":a,"col":b} give information of the position to make the move, starts at 0
        :return: (int) -2 if move is out of bound | -1 if position is already taken | 1 if move was succesfull performed
        """
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
        """
        checks if in the self.currentGame is already a winner when there are three moves in line for rows, columns or diagonals

        :return: (int) 1 if player 1 wins | 2 if player 2 wins | 3 if there is a draw | 0 in any other case
        """
        checksPlayerOne = np.where(self.currentGame == self.playerOne, 1 ,0)
        checksPlayerTwo = np.where(self.currentGame == self.playerTwo, 1 ,0)

        if self.checksPlayer(checksPlayerOne) == 1: return 1
        elif self.checksPlayer(checksPlayerTwo) == 1: return 2
        elif self.checksDraw() == 9: return 3
        else: return 0

    def checksDraw(self):
        """
        auxiliar method for validating a draw, if all the items of self.currentGame are filled with either self.playerOne
        or self.palyerTwo and method self.checksPlayer does not find a winner then is a draw

        :return: (int) number of spaces filled in selg.currentGame
        """
        counter = 0
        for row in self.currentGame:
            for item in row:
                counter += 1 if item != "-" else 0
        return counter

    def checksPlayer(self, movementsMatrix):
        """
        checks if there is a winner in rows columns or diagonals
        :param movementsMatrix: (numpy Array) 3x3 matrix filled with ones or zeros, depending on the player wanted to check

        :return: (int) 1 for winner | 0 if no winner
        """
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
        """
        try to create an automatic movement to be performend by the machine starts by defending moves and then
        applies attack movements

        :return: (void)
        """
        #try to create an automate movement
        checksThread = self.possibleWinner(self.playerOne)
        checksAttackWinner = self.possibleWinner(self.playerTwo)
        createAttackMove = self.attackMove()
        #If is the begining of game and center is available is taken for the machine
        if (self.moveNumber == 1 and self.currentGame[1,1] == '-'):
            self.makeMove({'row':1,'col':1})
        elif (self.moveNumber == 1 and self.currentGame[1,1] == self.playerOne): #opponent opens at center, then a corner is played
            self.makeMove({'row':0, 'col':2})
        elif(checksAttackWinner['status']): #Atacks if there is the change to complete 3 in a row
            self.makeMove(checksAttackWinner['move'])
        elif(checksThread['status']): # Adopts a defensive position if there are two taken places by adversary
            self.makeMove(checksThread['move'])
        elif(createAttackMove['status']): #attacks looking for the best chances
            self.makeMove(createAttackMove['move'])
        else:
            self.makeMove(self.randomChoose()) #other case choose a random available position

    def randomChoose(self):
        """
        Last option for machine, if there is no a possible winner move, just chooses the first available space

        :return: (dic)  {"row":a,"col":b} give information of the position to make the move, starts at 0
        """
        for i in range(self.currentGame.shape[0]):
            for j in range(self.currentGame[i,:].shape[0]):
                if self.currentGame[i,j] == "-":
                    return {'row':i,'col':j}

    def attackMove(self):
        """
        creates a scenario of possible winning for the machine, it searches for the first available space to perform
        a move and then calculates if it is likely to became a winner move

        :return: (dic) {'status': True, 'move': {"row": 0, "col": 0}} if the found movement is a possible winner also returns
                        the move to be make by the machine, if no movement was found returns {'status': False}
        """
        currentGameCopy = self.currentGame.copy()                           #a copy is performed to make easily calculations
        for i in range(self.currentGame.shape[0]):                          #try all the available spaces
            for j in range(self.currentGame[i,:].shape[0]):
                if self.currentGame[i,j] == "-":                            #first available space
                    self.currentGame[i, j] = self.playerTwo                 #make the move
                    checksWinnerPlay = self.possibleWinner(self.playerTwo)  #after the move is likely to get a winner?
                    if (checksWinnerPlay['status']):
                        self.currentGame = currentGameCopy                  #if a winner is found self.currentGame backs to original state
                        return checksWinnerPlay
                    else:
                        self.currentGame[i, j] = "-"                        #if not a winner the movement is back
        return {'status':False}

    def possibleWinner(self, player):
        """
        performs a search to know if in the current game for the selecter player there is a chance to make a final
        move and then have a winner, it is if there is two in a line of the desired player and the third in that line
        is available then is a possible winner or a defensive move

        :param player: (string) self.playerOne or self.playerTwo
        :return: (dict) {'status': True, 'move': {"row": 0, "col": 0}} if the found movement is a possible winner also returns
                        the move to be make by the machine, if no movement was found returns {'status': False}
        """
        checksPlayer = np.where(self.currentGame == player, 1, 0) #for easy calculations replace for 1 all self.currentGame selections are from desired player
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
        """
        Auxiliary function needed to perform a search in {axisValidate} direction if there are two in a line of the
        same player, this only validates for rows and columns

        :param arrayCheck: (numpy Array) 3x3 matrix with 1 if there is a move of the desired player 0 in other case
        :param axisValidate: (int) 0 for performing columns validation and 1 for rows validation
        :return: (dict) {'status': True, 'move': {"row": 0, "col": 0}} if the found movement is a possible winner also returns
                        the move to be make by the machine, if no movement was found returns {'status': False}
        """
        sumDim = np.sum(arrayCheck, axis=axisValidate)
        for i in range(sumDim.shape[0]):
            if sumDim[i] == 2: #there are two moves in a line
                dimToCheck = self.currentGame[:, i] if axisValidate == 0 else self.currentGame[i, :]
                notAlreadyPlayed = sum(np.where(dimToCheck == '-', 1, 0))  # if there is not "-" in the dimension continues
                if notAlreadyPlayed != 0:
                    for j in range(dimToCheck.shape[0]):
                        if dimToCheck[j] == '-': #the third element of the line is available
                            if axisValidate == 0:
                                return {'status': True, 'move': {"row": j, "col": i}}
                            else:
                                return {'status': True, 'move': {"row": i, "col": j}}
                            break
        return{'status':False}