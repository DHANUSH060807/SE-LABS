from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    has_pieces,
    has_legal_move,
    has_capture,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def run(self):
        print("Checkers — move: sr sc er ec")

        # Used when a capture sequence must continue.
        capture_piece = None

        while True:
            self.print_board()

            raw = input(f"{self.player}> ").strip().lower().split()

            if raw == ["q"]:
                return

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            start, end = (sr, sc), (er, ec)

            if capture_piece is not None and start != capture_piece:
                print("Invalid move.")
                continue

            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            must_capture = has_capture(self.board, self.player)

            is_capture = capture_move(
                self.board,
                self.player,
                start,
                end,
            )

            if must_capture and not is_capture:
                print("Invalid move.")
                continue

            if is_capture:
                piece_before = self.board[sr][sc]

                move_piece(self.board, start, end)

                # Remove the jumped opponent piece.
                mr = (sr + er) // 2
                mc = (sc + ec) // 2
                self.board[mr][mc] = "."

                # Promote immediately so a newly promoted king
                # can participate in the remainder of the sequence.
                promote(self.board)

                promoted = self.board[er][ec] != piece_before

                if promoted:
                    print(
                        f"{self.player} captured from "
                        f"({sr},{sc}) to ({er},{ec}) and promoted."
                    )
                else:
                    print(
                        f"{self.player} captured from "
                        f"({sr},{sc}) to ({er},{ec})."
                    )

                # Check whether the same piece has another capture.
                if has_capture(self.board, self.player, end):
                    capture_piece = end
                    continue

                capture_piece = None

            elif simple_move(self.board, self.player, start, end):
                piece_before = self.board[sr][sc]

                move_piece(self.board, start, end)
                promote(self.board)

                promoted = self.board[er][ec] != piece_before

                if promoted:
                    print(
                        f"{self.player} moved from "
                        f"({sr},{sc}) to ({er},{ec}) and promoted."
                    )
                else:
                    print(
                        f"{self.player} moved from "
                        f"({sr},{sc}) to ({er},{ec})."
                    )

                capture_piece = None
            # Change player after the move/complete capture sequence.
            self.player = "B" if self.player == "R" else "R"

            # Task 2: check whether the new player can continue.
            if (
                not has_pieces(self.board, self.player)
                or not has_legal_move(self.board, self.player)
            ):
                winner = "B" if self.player == "R" else "R"
                print(f"{winner} wins!")
                return    