import tkinter as tk
from functools import partial
import math

# Constants
PLAYER = "X"
AI = "O"
EMPTY = " "


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.board = [[EMPTY] * 3 for _ in range(3)]
        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.root,
                    text=EMPTY,
                    font=("Arial", 24),
                    width=5,
                    height=2,
                    command=partial(self.player_move, i, j),
                )
                self.buttons[i][j].grid(row=i, column=j)

    def player_move(self, i, j):
        if self.board[i][j] == EMPTY:
            self.board[i][j] = PLAYER
            self.buttons[i][j].config(text=PLAYER, state=tk.DISABLED)
            if self.check_winner(PLAYER):
                self.display_winner(f"Player {PLAYER} wins!")
            elif self.is_board_full():
                self.display_winner("It's a draw!")
            else:
                self.ai_move()

    def ai_move(self):
        best_score = float("-inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = AI
                    score = self.minimax(
                        self.board, 0, False, float("-inf"), float("inf")
                    )
                    self.board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.board[best_move[0]][best_move[1]] = AI
            self.buttons[best_move[0]][best_move[1]].config(text=AI, state=tk.DISABLED)
            if self.check_winner(AI):
                self.display_winner(f"Player {AI} wins!")

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(PLAYER):
            return -1
        elif self.check_winner(AI):
            return 1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            max_eval = float("-inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = AI
                        eval = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = EMPTY
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER
                        eval = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = EMPTY
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(
            self.board[i][2 - i] == player for i in range(3)
        ):
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != EMPTY for i in range(3) for j in range(3))

    def display_winner(self, message):
        winner_label = tk.Label(self.root, text=message, font=("Arial", 20))
        winner_label.grid(row=3, column=0, columnspan=3)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)
        play_again_button = tk.Button(
            self.root, text="Play Again", font=("Arial", 14), command=self.reset_board
        )
        play_again_button.grid(row=4, column=0, columnspan=3)

    def reset_board(self):
        self.board = [[EMPTY] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=EMPTY, state=tk.NORMAL)
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) > 2:
                widget.grid_forget()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
