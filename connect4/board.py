class Board:
    board = []
    boardWidth = 7
    boardHeight = 6

    def __init__(self):
        self.setBoard()

    def setBoard(self):
        for _ in range(self.boardHeight):
            self.board.append(['-']*self.boardWidth)

    def resetBoard(self):
        for row in range(self.boardHeight):
            for column in range(self.boardWidth):
                self.board[row][column] = '-'

    def printBoard(self):
        for i in range(self.boardHeight):
            print("| ", end="")
            print(*self.board[i], sep=" | ", end="")
            print(" |\n")

    def isValidColumn(self, column):
        return False if column < 0 or column >= self.boardWidth else True

    def getChip(self, row, column):
        return self.board[row][column]

    '''
        check can add new chip at column
        return can?(true, false), row chip added
    '''

    def canAddChip(self, column):
        if not self.isValidColumn(column):
            return False, -1
        for i in range(self.boardHeight - 1, -1, -1):  # from 5 to 0
            if self.board[i][column] == '-':
                return True, i
        return False, -1

    def addChip(self, chip, row, column):
        self.board[row][column] = chip

    def removeChip(self, row, column):
        self.board[row][column] = '-'

    def isWinner(self, chip):
        ticks = 0
        # Vertical
        for row in range(self.boardHeight - 3):
            for col in range(self.boardWidth):
                ticks = self.checkAdjacent(chip, row, col, 1, 0)
                if ticks == 4:
                    return True

        # Horizontal
        for row in range(self.boardHeight):
            for col in range(self.boardWidth - 3):
                ticks = self.checkAdjacent(chip, row, col, 0, 1)
                if ticks == 4:
                    return True

        # positive slope diagonal
        for row in range(self.boardHeight-3):
            for col in range(self.boardWidth - 3):
                ticks = self.checkAdjacent(chip, row, col, 1, 1)
                if ticks == 4:
                    return True

        # negative slope diagonal
        for row in range(3, self.boardHeight):
            for col in range(self.boardWidth - 5):
                ticks = self.checkAdjacent(chip, row, col, -1, 1)
                if ticks == 4:
                    return True

        return False

    def checkAdjacent(self, chip, row, col, deltaROW, deltaCOL):
        cnt = 0
        for _ in range(4):
            currentChip = self.getChip(row, col)
            if currentChip == chip:
                cnt += 1
            row += deltaROW
            col += deltaCOL
        return cnt
