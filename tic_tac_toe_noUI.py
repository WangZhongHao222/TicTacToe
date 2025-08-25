from datetime import datetime


class TicTacToeGame:
    def __init__(self):
        # Create an empty buttons_state
        self.buttons_state = [[" " for _ in range(9)] for _ in range(9)]
        self.sub_board_state = [" " for _ in range(9)]
        self.current_player = "Red"
        self.last_place = None
        self.move_log = []  # List to store the move log
        self.game_log = []  # List to store the game log

    def player_move(self):
        while True:
            try:
                i = int(input("Enter sub-board index (0-8): "))
                j = int(input("Enter cell index (0-8): "))
                if self.buttons_state[i][j] == " ":
                    break
                else:
                    print("Cell already taken. Try again.")
            except ValueError:
                print("Invalid input. Try again.")
        self.buttons_state[i][j] = self.current_player
        self.move_log.append((i, j))
        self.game_log.append((i, j))
        if self.check_sub_winner(self.current_player, i):
            self.sub_board_state[i] = self.current_player
            if self.check_winner(self.current_player):
                self.game_over(f"Player {self.current_player} wins!")
                return True
            elif self.check_tie():
                self.game_over("It's a tie!")
                return True
        elif self.check_sub_tie(i):
            self.sub_board_state[i] = "Tie"
            if self.check_tie():
                self.game_over("It's a tie!")
                return True
        self.current_player = "Blue" if self.current_player == "Red" else "Red"
        self.last_place = j
        return False

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

    def check_sub_tie(self, i):
        return " " not in self.buttons_state[i]

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

    def check_tie(self):
        return " " not in self.sub_board_state

    def game_over(self, message):
        file_name = f"tic_tac_toe_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(file_name, "w") as log_file:
            for entry in self.game_log:
                log_file.write(f"{entry},")
        print(message)
        print(f"Game log saved to {file_name}")

    def run(self):
        print("Welcome to Console Tic-Tac-Toe!")
        while True:
            self.print_board()
            print(f"Current player: {self.current_player}")
            if self.player_move():
                break


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
