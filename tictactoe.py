import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("400x500")
        self.window.configure(bg="#1C2526")

        self.board = [' ' for _ in range(10)]  # 1-9 for board positions
        self.player = 1
        self.mark = 'X'
        self.game = 0  # 0: Running, 1: Win, -1: Draw
        self.buttons = []
        self.is_single_player = False
        self.winning_positions = []  # To store winning move positions

        # Styling configurations
        self.button_style = {
            "font": ("Helvetica", 20, "bold"),
            "bg": "#2D3E50",
            "fg": "#FF4C4C",  # Red for X
            "activebackground": "#3A506B",
            "activeforeground": "#FF4C4C",
            "borderwidth": 0,
            "relief": "flat"
        }

        self.create_ui()

    def create_ui(self):
        # Title Label
        title = tk.Label(
            self.window,
            text="Tic-Tac-Toe",
            font=("Helvetica", 24, "bold"),
            bg="#1C2526",
            fg="#4DA8DA"  # Blue for title
        )
        title.pack(pady=20)

        # Mode Selection
        mode_frame = tk.Frame(self.window, bg="#1C2526")
        mode_frame.pack(pady=10)
        tk.Button(
            mode_frame,
            text="Single Player",
            font=("Helvetica", 12, "bold"),
            bg="#4DA8DA",
            fg="#FFFFFF",
            activebackground="#3A8CBA",
            borderwidth=0,
            command=lambda: self.set_mode(True)
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            mode_frame,
            text="Two Players",
            font=("Helvetica", 12, "bold"),
            bg="#4DA8DA",
            fg="#FFFFFF",
            activebackground="#3A8CBA",
            borderwidth=0,
            command=lambda: self.set_mode(False)
        ).pack(side=tk.LEFT, padx=5)

        # Game Board Frame
        board_frame = tk.Frame(self.window, bg="#1C2526")
        board_frame.pack(pady=20)

        # Create 3x3 grid of buttons
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = tk.Button(
                board_frame,
                text=" ",
                width=10,
                height=3,
                **self.button_style,
                command=lambda x=i: self.button_click(x)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)

        # Status Label
        self.status = tk.Label(
            self.window,
            text="Player's Turn (X)",
            font=("Helvetica", 14),
            bg="#1C2526",
            fg="#FFFFFF"
        )
        self.status.pack(pady=10)

        # Reset Button
        reset_btn = tk.Button(
            self.window,
            text="Reset Game",
            font=("Helvetica", 12, "bold"),
            bg="#FF4C4C",  # Red for reset button
            fg="#FFFFFF",
            activebackground="#D43F3F",
            activeforeground="#FFFFFF",
            borderwidth=0,
            relief="flat",
            command=self.reset_game
        )
        reset_btn.pack(pady=10)

    def set_mode(self, single_player):
        self.is_single_player = single_player
        self.reset_game()
        self.status.config(text="Player's Turn (X)")

    def button_click(self, pos):
        if self.board[pos] == ' ' and self.game == 0:
            self.board[pos] = self.mark
            self.buttons[pos-1].config(
                text=self.mark,
                fg="#FF4C4C" if self.mark == 'X' else "#4DA8DA"  # Red for X, Blue for O
            )
            self.check_win()
            if self.game == 0:
                self.player += 1
                self.mark = 'O' if self.player % 2 == 0 else 'X'
                self.status.config(
                    text="Computer's Turn (O)" if self.is_single_player and self.mark == 'O' else f"Player {2 if self.player % 2 == 0 else 1}'s Turn ({self.mark})"
                )
                if self.is_single_player and self.mark == 'O' and self.game == 0:
                    self.window.after(500, self.computer_move)
            elif self.game == 1:
                self.highlight_winning_move()
                winner = "Player" if self.player % 2 != 0 else "Computer" if self.is_single_player else "Player 2"
                if self.is_single_player:
                    message = "Awesome job, you won! 🎉" if winner == "Player" else "Hehe, the computer got you this time! 😄"
                else:
                    message = f"Congratulations, Player {1 if self.player % 2 != 0 else 2}! You won! 🎉"
                messagebox.showinfo("Game Over", message)
                self.disable_buttons()
            elif self.game == -1:
                messagebox.showinfo("Game Over", "It's a Draw! Good effort! 😊")
                self.disable_buttons()

    def computer_move(self):
        # Try to win
        move = self.find_best_move('O')
        if move:
            self.make_move(move)
            return
        # Block player from winning
        move = self.find_best_move('X')
        if move:
            self.make_move(move)
            return
        # Take center if available
        if self.board[5] == ' ':
            self.make_move(5)
            return
        # Take random available move
        available = [i for i in range(1, 10) if self.board[i] == ' ']
        if available:
            self.make_move(random.choice(available))

    def find_best_move(self, mark):
        win_conditions = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Columns
            (1, 5, 9), (3, 5, 7)              # Diagonals
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == mark != ' ' and self.board[c] == ' ':
                return c
            if self.board[a] == self.board[c] == mark != ' ' and self.board[b] == ' ':
                return b
            if self.board[b] == self.board[c] == mark != ' ' and self.board[a] == ' ':
                return a
        return None

    def make_move(self, pos):
        self.board[pos] = self.mark
        self.buttons[pos-1].config(
            text=self.mark,
            fg="#4DA8DA"  # Blue for O
        )
        self.check_win()
        if self.game == 0:
            self.player += 1
            self.mark = 'X'
            self.status.config(text="Player's Turn (X)")
        elif self.game == 1:
            self.highlight_winning_move()
            messagebox.showinfo("Game Over", "Hehe, the computer got you this time! 😄")
            self.disable_buttons()
        elif self.game == -1:
            messagebox.showinfo("Game Over", "It's a Draw! Good effort! 😊")
            self.disable_buttons()

    def check_win(self):
        win_conditions = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Rows
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Columns
            (1, 5, 9), (3, 5, 7)              # Diagonals
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                self.game = 1
                self.winning_positions = [a, b, c]
                return
        if all(self.board[i] != ' ' for i in range(1, 10)):
            self.game = -1

    def highlight_winning_move(self):
        for pos in self.winning_positions:
            self.buttons[pos-1].config(bg="#FFD700")  # Gold highlight for winning move

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self):
        self.board = [' ' for _ in range(10)]
        self.player = 1
        self.mark = 'X'
        self.game = 0
        self.winning_positions = []
        for btn in self.buttons:
            btn.config(text=" ", state="normal", **self.button_style)
        self.status.config(text="Player's Turn (X)" if self.is_single_player else "Player 1's Turn (X)")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()