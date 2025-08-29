import numpy as np


class TicTacToe:
    def __init__(self):
        self.board = np.array([" "] * 9)  # 3x3棋盘
        self.current_player = "X"  # 人类为X，AI为O
        self.game_over = False
        self.winner = None

    def print_board(self):
        """打印棋盘"""
        print("\n")
        for i in range(3):
            print(
                " "
                + self.board[i * 3]
                + " | "
                + self.board[i * 3 + 1]
                + " | "
                + self.board[i * 3 + 2]
            )
            if i < 2:
                print("-----------")
        print("\n")

    def make_move(self, position, player):
        """在指定位置落子"""
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        """检查是否有玩家获胜"""
        # 所有可能的获胜组合（行、列、对角线）
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # 行
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # 列
            [0, 4, 8],
            [2, 4, 6],  # 对角线
        ]

        for condition in win_conditions:
            if (
                self.board[condition[0]]
                == self.board[condition[1]]
                == self.board[condition[2]]
                != " "
            ):
                self.winner = self.board[condition[0]]
                self.game_over = True
                return True

        # 检查平局
        if " " not in self.board:
            self.game_over = True
            return True

        return False

    def minimax(self, board, depth, is_maximizing):
        """Minimax算法实现"""
        # 终端状态评估
        if self.evaluate(board) != 0:
            return self.evaluate(board)
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def evaluate(self, board):
        """评估棋盘状态：+10 AI赢，-10 人类赢，0 其他"""
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]

        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] == "O":
                return 10
            elif (
                board[condition[0]] == board[condition[1]] == board[condition[2]] == "X"
            ):
                return -10
        return 0

    def get_best_move(self):
        """找到最佳落子位置"""
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "

                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move

    def play(self):
        """开始游戏"""
        print("欢迎来到井字棋游戏！")
        print("位置编号如下：")
        print(" 0 | 1 | 2 ")
        print("-----------")
        print(" 3 | 4 | 5 ")
        print("-----------")
        print(" 6 | 7 | 8 ")
        print("\n您将使用X，AI使用O。请输入位置编号(0-8)落子。")

        while not self.game_over:
            self.print_board()

            if self.current_player == "X":
                # 人类回合
                try:
                    position = int(input("请输入落子位置(0-8): "))
                    if position < 0 or position > 8:
                        print("请输入0-8之间的数字！")
                        continue

                    if not self.make_move(position, "X"):
                        print("该位置已有棋子，请重新选择！")
                        continue

                except ValueError:
                    print("请输入有效数字！")
                    continue
            else:
                # AI回合
                print("AI思考中...")
                position = self.get_best_move()
                self.make_move(position, "O")
                print(f"AI在位置 {position} 落子")

            # 检查游戏状态
            if self.check_winner():
                self.print_board()
                if self.winner:
                    print(f"游戏结束！{self.winner} 获胜！")
                else:
                    print("游戏结束！平局！")
                break

            # 切换玩家
            self.current_player = "O" if self.current_player == "X" else "X"


# 运行游戏
if __name__ == "__main__":
    game = TicTacToe()
    game.play()
