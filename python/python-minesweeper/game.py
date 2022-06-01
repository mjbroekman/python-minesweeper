import sys
import argparse
import time

from cell import GameCell
from board import GameBoard

def main(argv):
    """Parse command-line arguments

    Args:
        argv: sys.argv
    """

    parser = argparse.ArgumentParser(description="Play MineSweeper in a Terminal window")
    parser.add_argument(
        "--rows",
        "-r",
        action="store",
        help="number of rows in the board",
        type=int
    )
    parser.add_argument(
        "--cols",
        "-c",
        action="store",
        help="number of columns in the baord",
        type=int
    )
    parser.add_argument(
        "--mines",
        "-m",
        action="store",
        help="number of mines to place",
        default=-1,
        type=int
    )
    args = parser.parse_args(argv)
    try:
        board = GameBoard(args.rows,args.cols,args.mines)
        while not board.complete():
            print(board)
            print("'open r c' -> Opens the cell at row r column c")
            print("'flag r c' -> Flags the cell at row r column c")
            move = input("Next move? ").split()
            if len(move) == 3 and (move[0] == "open" or move[0] == "flag"):
                if board.is_cell(move[1].upper(), move[2].upper()):
                    if move[0] == "open":
                        if not board.open(move[1].upper(), move[2].upper()):
                            board.reveal()
                            print(board)
                            print("BOOM! You hit a mine! A condolence letter will be sent to your next of kin.")
                            print("\n\n\n")
                            exit()
                    else:
                        board.flag(move[1].upper(), move[2].upper())
                else:
                    print("Invalid coordinates: " + move[1].upper() + " " + move[2].upper())
                    time.sleep(2.0)

    except ValueError as e:
        exit(e)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Exiting...')    