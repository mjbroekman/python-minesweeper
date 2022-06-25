"""PySweeper Game

Author:
    Maarten Broekman - https://github.com/mjbroekman

To play:
$ python -m pysweeper --rows ?? --cols ?? --mines ??

where:
  --rows is the number of rows you want (2 to 36, depending on the height of your terminal window)

  --cols is the number of columns you want (2 to 36, depending on the width of your terminal window)

  --mines is the number of 'splody cells you want ( between 1 and (rows*cols)-1 ) (optional)
       if you don't specifiy the number of mines, the game will choose it for you....

"""

import os
import sys
import argparse
import time

from . import board

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
        game = board.GameBoard(args.rows,args.cols,args.mines)
        while not game.complete():
            print(game)
            print("'(o)pen r c' -> Opens the cell at row r column c")
            print("'(f)lag r c' -> Flags the cell at row r column c")
            move = input("Next move? ").strip()

            if len(move) != 5:
                print("Incomplete or invalid command. Please use o (open) and f (flag) to play")
                time.sleep(2.0)
                continue

            cmd = move[0].lower()
            row = move[2].upper()
            col = move[4].upper()

            if cmd not in ("o", "f"):
                print("Invalid command '" + cmd + "'. Please use open (or o) and flag (or f) to play")
                time.sleep(2.0)
                continue

            if not game.is_cell(row, col):
                print("Invalid coordinates: " + row + " " + col)
                time.sleep(2.0)
                continue

            if cmd == "o":
                if not game.open(row, col):
                    game.reveal()
                    print(game)
                    print("BOOM! You hit a mine! A condolence letter will be sent to your next of kin.")
                    print("\n\n\n")
                    sys.exit()

            if cmd == "f":
                game.flag(row, col)

        game.reveal()
        print(game)
        print("CONGRATULATIONS! You successfully found all the mines without triggering one!")
        print("\n\n")
        sys.exit()

    except ValueError as e:
        sys.exit(e)


if __name__ == '__main__':
    try:
        if os.name == "nt":
            print('run MineSweeper.exe instead')
            sys.exit()

        main(sys.argv[1:])
    except (KeyboardInterrupt, EOFError):
        print('Exiting...')
        sys.exit()
