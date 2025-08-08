import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class TicTacToeGame:
    def __init__(self, game_type):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")

        # Create an empty buttons_state
        self.buttons_state = [[" " for _ in range(9)] for _ in range(9)]
        self.sub_board_state = [" " for _ in range(9)]
        self.current_player = (
            "Red"  # 'Red' represents player 1, 'Blue' represents player 2
        )
        self.player_color = {"Red": "#FFC0C0", "Blue": "#C0D6FF", "Tie": "#DFCBEF"}
        self.last_place = None

        # Define alternating colors for the board (like a chessboard pattern)
        self.light_color = "#FFFACD"
        self.colors = ["#F0E68C", "#F7E7A9"]
        self.move_log = []  # List to store the move log
        self.game_log = []  # List to store the game log

    # Function to update the current player's label
    def update_current_player(self):
        self.player_label2.config(text=f"{self.current_player}")
        self.player_button.config(
            bg=self.player_color[self.current_player], state="disabled"
        )

    # Function to update the possible moves on the small board
    def update_possible_moves(self):
        if self.last_place is None or self.sub_board_state[self.last_place] != " ":
            for i, small_button in enumerate(self.small_board):
                if self.sub_board_state[i] == " ":
                    small_button.config(bg=self.light_color, state="disabled")
                else:
                    small_button.config(
                        bg=self.player_color[self.sub_board_state[i]], state="disabled"
                    )
        else:
            for i, small_button in enumerate(self.small_board):
                if i == self.last_place:
                    small_button.config(bg=self.light_color, state="disabled")
                elif self.sub_board_state[i] == " ":
                    small_button.config(bg=self.colors[i % 2], state="disabled")
                else:
                    small_button.config(
                        bg=self.player_color[self.sub_board_state[i]], state="disabled"
                    )

    # Function to reset the game board
    def reset_board(self):
        self.buttons_state = [[" " for _ in range(9)] for _ in range(9)]
        self.sub_board_state = [" " for _ in range(9)]
        self.current_player = "Red"
        self.last_place = None
        self.move_log = []  # List to store the move log
        self.game_log = []  # List to store the game log
        self.update_possible_moves()
        self.update_current_player()
        for i, sub_board in enumerate(self.board):
            # Reset the text and background color
            for button in sub_board:
                button.config(text=" ", bg=self.colors[i % 2], state="normal")

    # Function to display a message and reset the game
    def game_over(self, message):
        file_name = f"tic_tac_toe_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(file_name, "w") as log_file:
            for entry in self.game_log:
                log_file.write(f"{entry},")
        messagebox.showinfo("Game Over", message + f"Game log saved to {file_name}")
        self.reset_board()

    # Function to handle player move
    def player_move(self, index):
        i, j = index
        if self.buttons_state[i][j] == " " and (
            self.last_place is None
            or self.sub_board_state[self.last_place] != " "
            or i == self.last_place
        ):
            # Update the buttons_state and color
            self.buttons_state[i][j] = self.current_player
            self.board[i][j].config(
                bg=self.player_color[self.current_player], state="disabled"
            )
            self.undo_button.config(bg=self.player_color[self.current_player])
            self.resign_button.config(
                bg=self.player_color["Blue" if self.current_player == "Red" else "Red"]
            )
            self.move_log.append(index)
            self.game_log.append(index)

            # Check for a win or tie in sub_board
            if self.check_sub_winner(self.current_player, i):
                self.sub_board_state[i] = self.current_player
                for button in self.board[i]:
                    button.config(
                        bg=self.player_color[self.current_player], state="disabled"
                    )
                if self.check_winner(self.current_player):
                    self.game_over(f"Player {self.current_player} wins!")
                    return
                elif self.check_tie():
                    self.game_over("It's a tie!")
                    return
            elif self.check_sub_tie(i):
                self.sub_board_state[i] = "Tie"
                if self.check_tie():
                    self.game_over("It's a tie!")
                    return

            # Switch players & mark the place
            self.current_player = "Blue" if self.current_player == "Red" else "Red"
            self.last_place = j
            self.update_current_player()
            self.update_possible_moves()

    # Function to handle undoing the last move
    def undo_last_move(self):
        if self.last_place is not None:
            i, j = self.move_log.pop()
            self.game_log.append((-1, -1))

            if self.sub_board_state[i] == " ":
                # Reset the button and enable it again
                self.buttons_state[i][j] = " "
                self.board[i][j].config(state="normal", bg=self.colors[i % 2])
            elif self.sub_board_state[i] == "Tie":
                # Reset the button and enable it again then Reset the sub board
                self.buttons_state[i][j] = " "
                self.board[i][j].config(state="normal", bg=self.colors[i % 2])
                self.sub_board_state[i] = " "
            else:
                # Reset the button and Reset the sub board
                self.buttons_state[i][j] = " "
                self.sub_board_state[i] = " "
                for k in range(9):
                    if self.buttons_state[i][k] == " ":
                        self.board[i][k].config(state="normal", bg=self.colors[i % 2])
                    else:
                        self.board[i][k].config(
                            state="disabled",
                            bg=self.player_color[self.buttons_state[i][k]],
                        )

            self.undo_button.config(
                bg=self.player_color["Blue" if self.current_player == "Red" else "Red"]
            )
            self.resign_button.config(bg=self.player_color[self.current_player])
            # Switch back to the previous player
            self.current_player = "Red" if self.current_player == "Blue" else "Blue"
            if self.move_log:
                self.last_place = self.move_log[-1][1]
            else:
                self.last_place = None
            self.update_current_player()
            self.update_possible_moves()

    # Function to handle resigning game
    def resign_game(self):
        winner = (
            "Blue" if self.current_player == "Red" else "Red"
        )  # The other player wins
        self.game_log.append((-2, -2))
        self.game_over(f"Player {self.current_player} resigned. Player {winner} wins!")

    # Function to check if there's a winner in sub_board
    def check_sub_winner(self, player, i):
        win_conditions = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # Rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # Columns
            (0, 4, 8),
            (2, 4, 6),  # Diagonals
        ]
        for condition in win_conditions:
            if (
                self.buttons_state[i][condition[0]]
                == self.buttons_state[i][condition[1]]
                == self.buttons_state[i][condition[2]]
                == player
            ):
                return True
        return False

    # Function to check if there's a tie in sub_board
    def check_sub_tie(self, i):
        return " " not in self.buttons_state[i]

    # Function to check if there's a winner
    def check_winner(self, player):
        win_conditions = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # Rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # Columns
            (0, 4, 8),
            (2, 4, 6),  # Diagonals
        ]
        for condition in win_conditions:
            if (
                self.sub_board_state[condition[0]]
                == self.sub_board_state[condition[1]]
                == self.sub_board_state[condition[2]]
                == player
            ):
                return True
        return False

    # Function to check for a tie
    def check_tie(self):
        return " " not in self.sub_board_state

    # Function to run the game
    def run(self):
        # Create a 3x3 grid of 3x3 grid buttons with background colors
        self.board = []
        for i in range(9):
            sub_board = []
            for j in range(9):
                button = tk.Button(
                    self.root,
                    font=("normal", 20),
                    width=5,
                    height=2,
                    bg=self.colors[i % 2],
                    command=lambda p=(i, j): self.player_move(p),
                )
                button.grid(row=i // 3 * 3 + j // 3, column=i % 3 * 3 + j % 3)
                sub_board.append(button)
            self.board.append(sub_board)

        # Create a frame for the side panel (to hold the label and small board)
        side_panel = tk.Frame(self.root)
        side_panel.grid(row=0, column=9, rowspan=10, padx=20, sticky="n")

        # Create a frame for the current player
        player_frame = tk.Frame(side_panel)
        player_frame.grid(row=0, column=0, pady=30, sticky="w")
        # Create a label and a button to show the current player
        self.player_label1 = tk.Label(player_frame, text="Player:", font=("normal", 20))
        self.player_label1.grid(row=0, column=0)
        self.player_label2 = tk.Label(
            player_frame, text=f"{self.current_player}", font=("normal", 20)
        )
        self.player_label2.grid(row=1, column=1)
        self.player_button = tk.Button(
            player_frame,
            font=("normal", 20),
            width=5,
            height=2,
            bg=self.player_color[self.current_player],
            state="disabled",
        )
        self.player_button.grid(row=1, column=2)

        # Create a frame for the small board (to show possible moves or info)
        small_board_frame = tk.Frame(side_panel)
        small_board_frame.grid(row=2, column=0, pady=30, sticky="w")
        # Create a label to show the playable button
        button_label = tk.Label(
            small_board_frame, text="Play Zone:", font=("normal", 20)
        )
        button_label.grid(row=0, column=0)
        # Create a small 3x3 grid to display possible moves or relevant info
        self.small_board = []
        for i in range(9):
            small_button = tk.Button(
                small_board_frame,
                font=("normal", 20),
                width=5,
                height=2,
                bg=self.light_color,
                state="disabled",
            )
            small_button.grid(row=1 + i // 3, column=1 + i % 3)
            self.small_board.append(small_button)

        # Create a frame for the current player
        button_frame = tk.Frame(side_panel)
        button_frame.grid(row=3, column=0, pady=30, sticky="w")
        # Create an Undo button
        self.undo_button = tk.Button(
            button_frame,
            text="Undo",
            font=("normal", 20),
            bg=self.player_color["Red" if self.current_player == "Blue" else "Blue"],
            command=self.undo_last_move,
        )
        self.undo_button.grid(row=0, column=0, padx=30, sticky="w")
        # Create a Resign button
        self.resign_button = tk.Button(
            button_frame,
            text="Resign",
            font=("normal", 20),
            bg=self.player_color[self.current_player],
            command=self.resign_game,
        )
        self.resign_button.grid(row=0, column=1, padx=60, sticky="e")

        # Start the GUI event loop
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = TicTacToeGame("0")
    game.run()
