from board import Board
from AI import AI
from player import Human


class Game:
    board = None
    human = None
    ai = None
    winner = False
    humanTurn = True
    currentRound = 1
    MAX_ROUNDS = 42

    def __init__(self) -> None:
        self.board = Board()
        self.human = Human()
        difficulty = int(input(
            "Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))
        self.ai = AI('X', difficulty)

    def play(self):
        print("Playing game...")
        self.board.printBoard()
        winner = "It's a DRAW!"
        while self.currentRound <= self.MAX_ROUNDS and not self.winner:
            if self.humanTurn:
                print("Player's turn...")
                playedChip = self.human.playTurn(self.board)
                self.winner = self.board.isWinner(self.human.chip)
                if self.winner:
                    winner = "PLAYER wins!"
                self.humanTurn = False
                print("Player played chip at column ", playedChip[1]+1)
            else:
                print("AI's turn...")
                playedChip = self.ai.playTurn(self.board)
                self.winner = self.board.isWinner(self.ai.chip)
                if self.winner:
                    winner = "AI wins!"
                self.humanTurn = True
                print("AI played chip at column ", playedChip[1]+1)
            self.currentRound += 1
            self.board.printBoard()
        return winner

    def reset(self):
        self.currentRound = 1
        self.winner = None
        self.humanTurn = True
        self.board.resetBoard()
        difficulty = int(input(
            "Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))
        self.ai.setDifficulty(difficulty)


def endGame(winner):
    print(winner, end=" ")
    userInput = input("Play again? (y/n)\n")
    return True if userInput == 'y' else False


if __name__ == '__main__':
    game = Game()
    winner = game.play()
    playAgain = endGame(winner)
    while playAgain:
        game.reset()
        winner = game.play()
        playAgain = endGame(winner)
