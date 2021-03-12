import random
class Game:


    def __init__(self,id):
        self.board = [['', '', ''],['', '', ''],['', '', '']]

        self.score = [0,0]
        self.playerTurn = random.randint(0, 1)
        self.gameReady = False
        self.id = id
        self.win = False
        self.tie = False
        print("Game Start, Wating people join game ..")

    def play(self, player, data):
        getData = data.split(",")
        if getData[0] == 'playerMove':
            if player == 0 and self.playerTurn == 0:
                self.board[int(getData[1])][int(getData[2])] = 'X'
                self.playerTurn = 1
            elif player == 1 and self.playerTurn == 1:
                self.board[int(getData[1])][int(getData[2])] = 'O'
                self.playerTurn = 0
            self.verifyWinner(player)
            if self.isBoardFull():
                self.tie = True
            else:
                self.tie = False

            print(self.board);
        elif getData[0] == 'resetBoard':
            self.win = False
            self.tie = False
            self.resetBoard()
            


    def connected(self):
        return self.gameReady

    def isWinner(self,player):
        if player == 0:
            role = 'X'
        elif player == 1:
            role = 'O'
        return ((self.board[0][0] == role and self.board[0][1] == role and self.board[0][2] == role) or
                (self.board[1][0] == role and self.board[1][1] == role and self.board[1][2] == role) or
                (self.board[2][0] == role and self.board[2][1] == role and self.board[2][2] == role) or
                (self.board[0][0] == role and self.board[1][0] == role and self.board[2][0] == role) or
                (self.board[0][1] == role and self.board[1][1] == role and self.board[2][1] == role) or
                (self.board[0][2] == role and self.board[1][2] == role and self.board[2][2] == role) or
                (self.board[0][0] == role and self.board[1][1] == role and self.board[2][2] == role) or
                (self.board[0][2] == role and self.board[1][1] == role and self.board[2][0] == role))

    def verifyWinner(self,player):
        if self.isWinner(player):
            if player == 0:
                self.score[0] += 1
            elif player == 1:
                self.score[1] += 1
            self.win = True
            return True


    def isBoardFull(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    return False
        return True

    def resetBoard(self):
        self.playerTurn = random.randint(0, 1)
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ''

