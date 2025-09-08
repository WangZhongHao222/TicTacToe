import numpy as np, time, random, sys

SIZE = 8
WIN = 5
EMPTY, ME, OPP = 0, 1, 2
DIRS = [(1, 0), (0, 1), (1, 1), (1, -1)]


def in_bounds(x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE


# ── 启发式打分：活四、冲四、活三……
PATTERN_SCORE = {
    (1, 1, 1, 1, 1): 50000,
    (0, 1, 1, 1, 1, 0): 25000,
    (1, 1, 1, 1, 0): 4320,
    (0, 1, 1, 1, 0): 720,
    (0, 1, 1, 0): 120,
    (0, 1, 0): 20,
    (2, 2, 2, 2, 2): -50000,
    (0, 2, 2, 2, 2, 0): -25000,
    (2, 2, 2, 2, 0): -4320,
    (0, 2, 2, 2, 0): -720,
    (0, 2, 2, 0): -120,
    (0, 2, 0): -20,
}


def pattern_score(line):
    s = 0
    for pat, val in PATTERN_SCORE.items():
        n = len(pat)
        for i in range(len(line) - n + 1):
            if tuple(line[i : i + n]) == pat:
                s += val
    return s


def eval_board(b):
    score = 0
    for dx, dy in DIRS:
        for x in range(SIZE):
            for y in range(SIZE):
                line = []
                for k in range(-4, 5):
                    nx, ny = x + k * dx, y + k * dy
                    if in_bounds(nx, ny):
                        line.append(b[nx, ny])
                score += pattern_score(line)
    return score


def is_win(b, p):
    for dx, dy in DIRS:
        for x in range(SIZE):
            for y in range(SIZE):
                if all(
                    in_bounds(x + k * dx, y + k * dy) and b[x + k * dx, y + k * dy] == p
                    for k in range(WIN)
                ):
                    return True
    return False


def moves(b):
    cand = [(x, y) for x in range(SIZE) for y in range(SIZE) if b[x, y] == 0]
    # 靠近棋子优先
    cand.sort(
        key=lambda m: min(
            abs(m[0] - i) + abs(m[1] - j)
            for i in range(SIZE)
            for j in range(SIZE)
            if b[i, j] != 0
        )
    )
    return cand[: min(20, len(cand))]  # 只取前 10 个候选


def negamax(b, depth, alpha, beta, player):
    if depth == 0 or is_win(b, ME) or is_win(b, OPP):
        return eval_board(b) * player
    best = -1e9
    for x, y in moves(b):
        b[x, y] = ME if player == 1 else OPP
        val = -negamax(b, depth - 1, -beta, -alpha, -player)
        b[x, y] = 0
        best = max(best, val)
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return best


def ai_move(b, max_depth=4):
    best, move = -1e9, None
    for depth in range(1, max_depth + 1):
        for x, y in moves(b):
            b[x, y] = ME
            val = -negamax(b, depth - 1, -1e9, 1e9, -1)
            b[x, y] = 0
            if val > best:
                best, move = val, (x, y)
    return move


# ── CLI 演示
if __name__ == "__main__":
    board = np.zeros((SIZE, SIZE), dtype=int)
    while True:
        print(board)
        while True:
            try:
                x, y = map(int, input("你下 (x y): ").split())
            except:
                continue
            if in_bounds(x, y) and board[x, y] == EMPTY:
                break
        board[x, y] = OPP
        if is_win(board, OPP):
            print("你赢了")
            break
        t = time.time()
        mx, my = ai_move(board)
        print("AI 用时 %.2fs 落子 %d %d" % (time.time() - t, mx, my))
        board[mx, my] = ME
        if is_win(board, ME):
            print("AI 赢")
            break
