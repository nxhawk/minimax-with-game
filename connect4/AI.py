import math

INFINITY = math.inf


class AI:
    depth = 0
    currentDepth = 0
    chip = "X"

    def __init__(self, chip='X', difficulty=1):
        self.chip = chip
        self.depth = difficulty

    def setDifficulty(self, difficulty):
        self.depth = difficulty
        self.currentDepth = 0

    def playTurn(self, board):
        move = self.alphaBetaSearch(board)
        board.addChip(self.chip, move[0], move[1])
        return move

    def evaluateHeuristic(self, board):
        horizontalScore = 0
        verticalScore = 0
        diagonal1Score = 0
        diagonal2Score = 0

        # vertical
        for row in range(board.boardHeight - 3):
            for column in range(board.boardWidth):
                score = self.scorePosition(board, row, column, 1, 0)
                verticalScore += score

        # Horizontal
        for row in range(board.boardHeight):
            for column in range(board.boardWidth - 3):
                score = self.scorePosition(board, row, column, 0, 1)
                horizontalScore += score

        # Diagonal 1
        for row in range(board.boardHeight - 3):
            for column in range(board.boardWidth - 3):
                score = self.scorePosition(board, row, column, 1, 1)
                diagonal1Score += score

        # Diagonal 1
        for row in range(3, board.boardHeight):
            for column in range(board.boardWidth - 3):
                score = self.scorePosition(board, row, column, -1, 1)
                diagonal2Score += score

        return horizontalScore + verticalScore + diagonal1Score + diagonal2Score

    def scorePosition(self, board, row, column, deltaROW, deltaCOL):
        '''
            Hueristic evaluation 
            for current state
            +1000, +100, +10, +1 for 4-,3-,2-,1-in-a-line for AI player
            -1000, -100, -10, -1 for 4-,3-,2-,1-in-a-line for human player
            0 otherwise
        '''
        humanScore = AIScore = humanPoints = AIPoints = 0
        for _ in range(4):
            currentChip = board.getChip(row, column)
            if currentChip == 'X':
                AIPoints += 1
            elif currentChip == 'O':
                humanPoints += 1

            row += deltaROW
            column += deltaCOL

        if humanPoints == 1:
            humanScore = -1
        elif humanPoints == 2:
            humanScore = -10
        elif humanPoints == 3:
            humanScore = -100
        elif humanPoints == 4:
            humanScore = -1000

        if AIPoints == 1:
            AIScore = -1
        elif AIPoints == 2:
            AIScore = -10
        elif AIPoints == 3:
            AIScore = -100
        elif AIPoints == 4:
            AIScore = -1000

        return AIScore + humanScore

    def generateMoves(self, board):
        possibleMovies = []
        for column in range(board.boardWidth):
            move = board.canAddChip(column)
            if move[0]:
                possibleMovies.append((move[1], column))  # (row, column)
        return possibleMovies

    def alphaBetaSearch(self, state):
        self.currentDepth = 0
        scores = []
        bestAction = None
        v = max_value = -INFINITY
        alpha = -INFINITY
        beta = INFINITY
        actions = self.generateMoves(state)
        for action in actions:
            state.addChip(self.chip, action[0], action[1])
            v = self.minValue(state, alpha, beta)
            scores.append(v)
            if v > max_value:
                max_value = v
                bestAction = action
                alpha = max(alpha, v)
            self.currentDepth -= 1
            state.removeChip(action[0], action[1])
        if len(scores) == 1:
            bestAction = actions[0]
        return bestAction

    def maxValue(self, state, alpha, beta):
        self.currentDepth += 1
        actions = self.generateMoves(state)
        if not actions or self.currentDepth >= self.depth:
            return self.evaluateHeuristic(state)

        v = -INFINITY
        for action in actions:
            state.addChip('O', action[0], action[1])
            v = max(v, self.minValue(state, alpha, beta))
            if v >= beta:
                self.currentDepth -= 1
                state.removeChip(action[0], action[1])
                return v
            alpha = max(alpha, v)
            self.currentDepth -= 1
            state.removeChip(action[0], action[1])
        return v

    def minValue(self, state, alpha, beta):
        self.currentDepth += 1
        actions = self.generateMoves(state)
        if not actions or self.currentDepth >= self.depth:
            return self.evaluateHeuristic(state)

        v = INFINITY
        for action in actions:
            state.addChip('O', action[0], action[1])
            v = min(v, self.maxValue(state, alpha, beta))
            if v <= alpha:
                self.currentDepth -= 1
                state.removeChip(action[0], action[1])
                return v
            beta = min(beta, v)
            self.currentDepth -= 1
            state.removeChip(action[0], action[1])
        return v
