import time

NROW = 4
NCOL = 3
NWIN = 3
firstPlay = True


class Game:
    def __init__(self, row, col, win):
        self.initialize_game(row, col, win)

    def initialize_game(self, row, col, win):
        global firstPlay
        firstPlay = True
        self.NROW = row
        self.NCOL = col
        self.NWIN = win

        # init state all ['.'] : none player
        self.current_state = []
        for _ in range(self.NROW):
            self.current_state.append(['.']*self.NCOL)

        # player turn X start game
        self.player_turn = 'X'

    def draw_board_game(self):
        for i in range(self.NROW):
            for j in range(self.NCOL):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    # can? chosen (x, y)
    def is_valid(self, x, y):
        if x < 0 or y < 0 or x > self.NROW - 1 or y > self.NCOL - 1:
            return False
        return self.current_state[x][y] == '.'

    def is_end(self) -> (str):
        # Vertical win
        for col in range(self.NCOL):
            for row in range(self.NROW - self.NWIN + 1):
                X_win = O_win = True
                for curr in range(self.NWIN):
                    if self.current_state[row + curr][col] != 'O':
                        O_win = False
                    if self.current_state[row + curr][col] != 'X':
                        X_win = False
                if X_win:
                    return 'X'
                if O_win:
                    return 'O'

        # Horizontal win
        for row in range(self.NROW):
            for col in range(self.NCOL - self.NWIN + 1):
                X_win = O_win = True
                for curr in range(self.NWIN):
                    if self.current_state[row][col + curr] != 'O':
                        O_win = False
                    if self.current_state[row][col + curr] != 'X':
                        X_win = False
                if X_win:
                    return 'X'
                if O_win:
                    return 'O'
        # Main diagonal win
        for row in range(self.NROW - self.NWIN + 1):
            for col in range(self.NCOL - self.NWIN + 1):
                X_win = O_win = True
                for curr in range(self.NWIN):
                    if self.current_state[row + curr][col + curr] != 'O':
                        O_win = False
                    if self.current_state[row + curr][col + curr] != 'X':
                        X_win = False
                if X_win:
                    return 'X'
                if O_win:
                    return 'O'
        # Second diagonal win
        for row in range(self.NROW - self.NWIN + 1):
            for col in range(self.NCOL - 1, self.NWIN - 2, -1):
                X_win = O_win = True
                for curr in range(self.NWIN):
                    if self.current_state[row + curr][col - curr] != 'O':
                        O_win = False
                    if self.current_state[row + curr][col - curr] != 'X':
                        X_win = False
                if X_win:
                    return 'X'
                if O_win:
                    return 'O'
        # Tie
        for row in range(NROW):
            for col in range(NCOL):
                if self.current_state[row][col] == '.':
                    return None
        return '.'

    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        px = py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(NROW):
            for j in range(NCOL):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, _, _) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    if maxv >= beta:
                        return (maxv, px, py)
                    if maxv > alpha:
                        alpha = maxv
        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta):
        minv = 2
        px = py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(NROW):
            for j in range(NCOL):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, _, _) = self.min_alpha_beta(alpha, beta)
                    if minv > m:
                        minv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    if alpha >= minv:
                        return (minv, px, py)
                    if beta > minv:
                        beta = minv
        return (minv, px, py)

    def play(self):
        global firstPlay
        while True:
            self.draw_board_game()
            self.result = self.is_end()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return

            if self.player_turn == 'X':

                while True:
                    if firstPlay == False:
                        start = time.time()
                        (_, qx, qy) = self.min_alpha_beta(-2, 2)
                        end = time.time()
                        print('Evaluation time: {}s'.format(
                            round(end - start, 7)))
                        print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                    else:
                        firstPlay = False

                    px = int(input('Insert the X coordinate: '))
                    py = int(input('Insert the Y coordinate: '))

                    qx = px
                    qy = py

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            else:
                (_, px, py) = self.max_alpha_beta(-2, 2)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'


def main():
    g = Game(NROW, NCOL, NWIN)
    g.play()


if __name__ == '__main__':
    main()
