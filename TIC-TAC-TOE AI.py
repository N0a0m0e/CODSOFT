import numpy as np

# Constants for players
PLAYER_X = "X"
PLAYER_O = "O"

class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), ' ')
        self.current_player = PLAYER_X

    def print_board(self):
        print("\n".join([" | ".join(row) for row in self.board]))
        print()

    def check_winner(self):
        # Check rows, columns, and diagonals for a winner
        for i in range(3):
            if self.board[i, :].tolist().count(PLAYER_X) == 3 or self.board[:, i].tolist().count(PLAYER_X) == 3:
                return PLAYER_X
            if self.board[i, :].tolist().count(PLAYER_O) == 3 or self.board[:, i].tolist().count(PLAYER_O) == 3:
                return PLAYER_O
        if (self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != ' ') or \
           (self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != ' '):
            return self.board[1, 1]
        return None

    def is_board_full(self):
        return ' ' not in self.board

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        if winner == PLAYER_X:
            return -1
        elif winner == PLAYER_O:
            return 1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -np.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i, j] == ' ':
                        self.board[i, j] = PLAYER_O
                        score = self.minimax(depth + 1, False)
                        self.board[i, j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = np.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i, j] == ' ':
                        self.board[i, j] = PLAYER_X
                        score = self.minimax(depth + 1, True)
                        self.board[i, j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def best_move(self):
        best_score = -np.inf
        move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == ' ':
                    self.board[i, j] = PLAYER_O
                    score = self.minimax(0, False)
                    self.board[i, j] = ' '
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def play(self):
        while True:
            self.print_board()
            if self.current_player == PLAYER_X:
                row, col = map(int, input("Enter your move (row and column): ").split())
                if self.board[row, col] != ' ':
                    print("Invalid move! Try again.")
                    continue
            else:
                row, col = self.best_move()

            self.board[row, col] = self.current_player
            winner = self.check_winner()

            if winner:
                self.print_board()
                print(f"Player {winner} wins!")
                break
            elif self.is_board_full():
                self.print_board()
                print("It's a draw!")
                break

            # Switch players
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

if __name__ == "__main__":
    game = TicTacToe()
    game.play()
