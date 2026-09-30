SIZE = 8


def opponent(player):
    return "B" if player == "R" else "R"


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]
    if piece not in (player, player + "K"):
        return False

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False

    # Kings can move in both directions.
    if piece == player + "K":
        return True

    direction = -1 if player == "R" else 1
    return er - sr == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]
    if piece not in (player, player + "K"):
        return False

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    # Kings can capture in both directions.
    if piece != player + "K":
        direction = -1 if player == "R" else 1
        if er - sr != 2 * direction:
            return False

    mr, mc = (sr + er) // 2, (sc + ec) // 2
    enemy = opponent(player)

    return board[mr][mc] in (enemy, enemy + "K")


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"


def has_pieces(board, player):
    return any(
        cell in (player, player + "K")
        for row in board
        for cell in row
    )


def has_capture(board, player, only_start=None):
    for r in range(SIZE):
        for c in range(SIZE):
            if only_start is not None and (r, c) != only_start:
                continue

            if board[r][c] not in (player, player + "K"):
                continue

            start = (r, c)

            for er in range(SIZE):
                for ec in range(SIZE):
                    if capture_move(board, player, start, (er, ec)):
                        return True

    return False


def has_legal_move(board, player):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] not in (player, player + "K"):
                continue

            start = (r, c)

            for er in range(SIZE):
                for ec in range(SIZE):
                    end = (er, ec)

                    if capture_move(board, player, start, end):
                        return True

                    if simple_move(board, player, start, end):
                        return True

    return False