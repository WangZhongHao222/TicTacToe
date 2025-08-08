import tkinter as tk
from datetime import datetime


class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.colors = ["#F0E68C", "#F7E7A9"]
        self.board = []
        self.last_move = None
        self.current_player = "Red"
        self.move_log = []

        self.player_label = tk.Label(
            root, text="Current Player: Red", font=("normal", 20)
        )
        self.player_label.grid(row=0, column=10, padx=20, sticky="nw")

        self.undo_button = tk.Button(
            root,
            text="Undo Last Move",
            font=("normal", 20),
            command=self.undo_last_move,
        )
        self.undo_button.grid(row=1, column=10, padx=20, sticky="nw")

        self.save_button = tk.Button(
            root, text="Save Log", font=("normal", 20), command=self.save_log_to_file
        )
        self.save_button.grid(row=2, column=10, padx=20, sticky="nw")

        self.resign_button = tk.Button(
            root, text="Resign", font=("normal", 20), command=self.resign_game
        )
        self.resign_button.grid(row=3, column=10, padx=20, sticky="nw")

        self.log_textbox = tk.Text(
            root, height=10, width=40, font=("normal", 12), state="disabled"
        )
        self.log_textbox.grid(row=4, column=10, padx=20, sticky="nw")

        self.create_board()

    def create_board(self):
        for i in range(9):
            sub_board = []
            for j in range(9):
                button = tk.Button(
                    self.root,
                    text=" ",
                    font=("normal", 20),
                    width=5,
                    height=2,
                    bg=self.colors[(i // 3 + j // 3) % 2],
                    command=lambda p=(i, j): self.player_move(p),
                )
                button.grid(row=i // 3 * 3 + j // 3, column=i % 3 * 3 + j % 3)
                sub_board.append(button)
            self.board.append(sub_board)

    def player_move(self, p):
        i, j = p
        button = self.board[i][j]
        if button["text"] == " ":
            button["text"] = "X" if self.current_player == "Red" else "O"
            button.config(
                fg="red" if self.current_player == "Red" else "blue", state="disabled"
            )
            self.log_move(i, j)
            self.last_move = (i, j)
            self.current_player = "Blue" if self.current_player == "Red" else "Red"
            self.update_current_player()

    def undo_last_move(self):
        if self.last_move is not None:
            i, j = self.last_move
            button = self.board[i][j]
            button.config(
                text=" ",
                state="normal",
                fg="black",
                bg=self.colors[(i // 3 + j // 3) % 2],
            )
            self.current_player = "Red" if self.current_player == "Blue" else "Red"
            self.update_current_player()
            self.move_log.pop()
            self.update_log_display()
            self.last_move = None

    def log_move(self, row, col):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"{timestamp} - {self.current_player}: Move to ({row}, {col})"
        self.move_log.append(log_entry)
        self.update_log_display()

    def update_current_player(self):
        self.player_label.config(text=f"Current Player: {self.current_player}")

    def update_log_display(self):
        self.log_textbox.config(state="normal")
        self.log_textbox.delete(1.0, tk.END)
        self.log_textbox.insert(tk.END, "\n".join(self.move_log))
        self.log_textbox.config(state="disabled")

    def save_log_to_file(self):
        file_name = f"tic_tac_toe_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(file_name, "w") as log_file:
            log_file.write("Tic-Tac-Toe Game Log\n")
            log_file.write("===================\n\n")
            for entry in self.move_log:
                log_file.write(entry + "\n")
        print(f"Game log saved to {file_name}")

    def resign_game(self):
        winner = "Blue" if self.current_player == "Red" else "Red"
        log_entry = f"{datetime.now().strftime('%H:%M:%S')} - {self.current_player} resigned. {winner} wins!"
        self.move_log.append(log_entry)
        self.update_log_display()
        for row in self.board:
            for button in row:
                button.config(state="disabled")
        self.player_label.config(text=f"{winner} wins by resignation")


# Initialize the main window
root = tk.Tk()
root.title("Tic-Tac-Toe with Resign, Undo, and Log")

# Define alternating colors for the grid
colors = ["#F0E68C", "#F7E7A9"]

# Create an empty board structure (9x9 grid split into 9 sub-boards)
board = []
last_move = None  # To store the last move
current_player = "Red"
move_log = []  # List to store the game log


# Function to handle player moves
def player_move(p):
    global last_move, current_player
    i, j = p
    button = board[i][j]

    # Make sure the button hasn't already been clicked
    if button["text"] == " ":
        button["text"] = "X" if current_player == "Red" else "O"
        button.config(fg="red" if current_player == "Red" else "blue", state="disabled")

        # Log the move
        log_move(i, j)

        # Store the last move
        last_move = (i, j)

        # Switch the player after the move
        current_player = "Blue" if current_player == "Red" else "Red"
        update_current_player()


# Function to handle undoing the last move
def undo_last_move():
    global last_move, current_player
    if last_move is not None:
        i, j = last_move
        button = board[i][j]

        # Reset the button text and enable it again
        button.config(
            text=" ", state="normal", fg="black", bg=colors[(i // 3 + j // 3) % 2]
        )

        # Switch back to the previous player
        current_player = "Red" if current_player == "Blue" else "Red"
        update_current_player()

        # Remove the last move from the log
        move_log.pop()
        update_log_display()

        # Clear the last move
        last_move = None


# Function to log each move
def log_move(row, col):
    global move_log
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"{timestamp} - {current_player}: Move to ({row}, {col})"
    move_log.append(log_entry)
    update_log_display()


# Function to update the current player label
def update_current_player():
    player_label.config(text=f"Current Player: {current_player}")


# Function to update the log display
def update_log_display():
    log_textbox.config(state="normal")  # Enable editing to update the text
    log_textbox.delete(1.0, tk.END)  # Clear current log display
    log_textbox.insert(tk.END, "\n".join(move_log))  # Insert the updated log
    log_textbox.config(state="disabled")  # Disable editing after updating


# Function to save the log to a file
def save_log_to_file():
    file_name = f"tic_tac_toe_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(file_name, "w") as log_file:
        log_file.write("Tic-Tac-Toe Game Log\n")
        log_file.write("===================\n\n")
        for entry in move_log:
            log_file.write(entry + "\n")
    print(f"Game log saved to {file_name}")


# Function to handle resignation
def resign_game():
    global current_player
    winner = "Blue" if current_player == "Red" else "Red"  # The other player wins
    log_entry = f"{datetime.now().strftime('%H:%M:%S')} - {current_player} resigned. {winner} wins!"
    move_log.append(log_entry)
    update_log_display()

    # Disable all buttons on the board to prevent further moves
    for row in board:
        for button in row:
            button.config(state="disabled")

    # Display the winner
    player_label.config(text=f"{winner} wins by resignation")


# Create the main 9x9 grid
for i in range(9):
    sub_board = []
    for j in range(9):
        button = tk.Button(
            root,
            text=" ",
            font=("normal", 20),
            width=5,
            height=2,
            bg=colors[(i // 3 + j // 3) % 2],  # Alternate colors based on the sub-grid
            command=lambda p=(i, j): player_move(p),
        )
        # Grid placement for sub-boards (i//3*3 + j//3) determines the row and column for each sub-board
        button.grid(row=i // 3 * 3 + j // 3, column=i % 3 * 3 + j % 3)
        sub_board.append(button)
    board.append(sub_board)

# Create a label to show the current player
player_label = tk.Label(root, text="Current Player: Red", font=("normal", 20))
player_label.grid(row=0, column=10, padx=20, sticky="nw")

# Create an Undo button
undo_button = tk.Button(
    root, text="Undo Last Move", font=("normal", 20), command=undo_last_move
)
undo_button.grid(row=1, column=10, padx=20, sticky="nw")

# Create a Save Log button
save_button = tk.Button(
    root, text="Save Log", font=("normal", 20), command=save_log_to_file
)
save_button.grid(row=2, column=10, padx=20, sticky="nw")

# Create a Resign button
resign_button = tk.Button(root, text="Resign", font=("normal", 20), command=resign_game)
resign_button.grid(row=3, column=10, padx=20, sticky="nw")

# Create a Text widget to display the move log
log_textbox = tk.Text(root, height=10, width=40, font=("normal", 12), state="disabled")
log_textbox.grid(row=4, column=10, padx=20, sticky="nw")

# Start the main loop
root.mainloop()
