"""GameBoard class

Author:
    Maarten Broekman - https://github.com/mjbroekman

Raises:
    ValueError if the screen size doesn't fit a board or if there are too many mines or if the board is too wide/tall

Returns:
    GameBoard: a GameBoard object
"""
import os
import random
import time

from . import cell

COORD_LIST = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class GameBoard:
    """Game board class.
    """
    _board_cells = []
    _mine_cells = []
    _board = {}
    _max_r = None
    _max_c = None

    def __init__(self, r_size: int, c_size: int, num_mines=-1):
        """Create the game board

        Args:
            r_size (int): Horizontal size
            c_size (int): Vertical size
            num_mines (int, optional): Number of mines. Defaults to -1 (random).
        """
        self._get_term_size()
        self.r_size = r_size
        self.c_size = c_size
        self.mines_left = num_mines
        self._create_board()


    def __repr__(self):
        """Representation matters

        Returns:
            str: String representation of the board
        """
        if os.name == "posix":
            _ = os.system('clear')
        elif os.name == "nt":
            _ = os.system('cls')
        else:
            pass

        _display = " "
        if self.r_size > 9:
            _display += " " * int(((self.c_size * 2) - 9) / 2)
        _display += "PySweeper\n"
        _display += "  "
        _display += "".join([ " " + c for c in COORD_LIST[:self.c_size] ])
        _display += "\n"
        _display += " /" + "-" * ((self.c_size * 2)) + "\\"
        _display += "   Mines Left: " + str(self.mines_left - self._num_flagged()) + "\n"
        for r in COORD_LIST[:self.r_size]:
            _display += r + "|"
            for c in COORD_LIST[:self.c_size]:
                _display += str(self._board[(r,c)])
            _display += "|\n"
        _display += " \\" + "-" * ((self.c_size * 2))  + "/\n"
        return _display


    def _get_term_size(self):
        """(private) Get the size of the terminal for boundary checking

        Raises:
            ValueError: if the screen is too narrow or too short
        """
        if os.get_terminal_size()[0] > 46:
            self._max_r = 36
        else:
            self._max_r = os.get_terminal_size()[0] - 10

        if os.get_terminal_size()[1] > 41:
            self._max_c = 36
        else:
            self._max_c = os.get_terminal_size()[1] - 7

        if self._max_r < 0:
            raise ValueError("Screen is too narrow. Minimum screen width is 10 columns.")

        if self._max_c < 0:
            raise ValueError("Screen is too short. Minimum screen height is 7 rows.")


    @property
    def mines_left(self) -> int:
        """(property) Number of mines to find

        Returns:
            int: number of mines remaining
        """
        return self._mines_left


    @mines_left.setter
    def mines_left(self, mines: int):
        """(setter) Set the number of mines remaining

        Args:
            mines (int): Number of mines left to flag

        Raises:
            ValueError: Trying to stuff too many mines into the board
        """
        if mines < 1:
            mines = random.randrange(1, (self.r_size * self.c_size))

        if mines > ((self.r_size * self.c_size) - 1):
            raise ValueError("Too many mines to fit. Must be between 1 and " + str((self.r_size * self.c_size) - 1))

        self._mines_left = mines


    @property
    def r_size(self) -> int:
        """(property) Get the size in rows of the board

        Returns:
            int: number of rows
        """
        return self._r_size


    @r_size.setter
    def r_size(self, size: int):
        """(setter) Set the size in rows of the board

        Args:
            size (int): number of rows

        Raises:
            ValueError: Given size is outside the bounds
        """
        try:
            if 1 < size <= self._max_r:
                self._r_size = size
            else:
                raise ValueError("Board height must be between 2 and " + str(self._max_r) + " cells.")
        except Exception as e:
            raise ValueError("Board height must be between 2 and " + str(self._max_r) + " cells.") from e


    @property
    def c_size(self) -> int:
        """(property) Get the size in columns of the board

        Returns:
            int: number of columns
        """
        return self._c_size


    @c_size.setter
    def c_size(self, size: int):
        """Set the size in columns of the board

        Args:
            size (int): number of columns

        Raises:
            ValueError: Given size is outside the bounds
        """
        try:
            if 1 < size <= self._max_c:
                self._c_size = size
            else:
                raise ValueError("Board width must be between 2 and " + str(self._max_c) + " cells")
        except Exception as e:
            raise ValueError("Board width must be between 2 and " + str(self._max_c) + " cells") from e


    def _create_board(self):
        """Creates the board
        """
        self._board_cells = [ (r,c) for r in COORD_LIST[:self.r_size] for c in COORD_LIST[:self.c_size] ]
        self._mine_cells = random.sample(self._board_cells, self.mines_left)
        for _cell in self._board_cells:
            if _cell in self._mine_cells:
                self._board[_cell] = cell.GameCell(name="M",mine=True)
            else:
                _neighbor_mines = list(filter(lambda cell: cell in self._mine_cells, self._get_neighbors(_cell)))
                self._board[_cell] = cell.GameCell(name=str(len(_neighbor_mines)),mine=False)


    def _get_neighbors(self,_cell,flagged=False,unmarked=False) -> list:
        """Get the neighboring cells in the board
           based on https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list

        Args:
            _cell    (tuple) : cell coordinates (row, col)
            flagged  (bool)  : Only return neighboring cells that have been flagged as potential mines
            unmarked (bool)  : Only return neighboring cells that have NOT been opened nor flagged

        Returns:
            list: list of neighboring cells
        """
        _cell_r = COORD_LIST.index(_cell[0])
        _cell_c = COORD_LIST.index(_cell[1])
        _neighbors = [(COORD_LIST[r2],COORD_LIST[c2])
                         for r2 in range(_cell_r-1,_cell_r+2)
                             for c2 in range(_cell_c-1,_cell_c+2)
                                 if ((_cell_r != r2 or _cell_c != c2) and
                                     (0 <= r2 <= self.r_size - 1) and
                                     (0 <= c2 <= self.c_size - 1)
                                     )]

        if unmarked:
            return list(filter(lambda cell: not self._board[cell].is_flagged() and not self._board[cell].is_open(), _neighbors))

        if flagged:
            return list(filter(lambda cell: self._board[cell].is_flagged(), _neighbors))


        return _neighbors


    def open(self, row: str, col: str) -> bool:
        """Open (possibly recursively) a cell

        Args:
            row (str): row coordinate
            col (str): column coordinate

        Returns:
            bool: Whether the game is still going
        """
        if self._board[(row, col)].is_flagged():
            print("Use f " + str(row) + " " + str(col) + " to remove the flag on this cell before opening.")
            time.sleep(2.0)
            return True

        if self._board[(row, col)].is_open():
            if int(self._board[(row, col)].name()) == len(self._get_neighbors((row, col),flagged=True)):
                for _unopened in self._get_neighbors((row, col),unmarked=True):
                    self.open(_unopened[0],_unopened[1])
            return True

        if not self._board[(row, col)].open():
            if self._board[(row, col)].is_safe():
                #for _cell in list(filter(lambda cell: not self._board[cell].is_open(), self._get_neighbors((row, col)))):
                for _cell in self._get_neighbors((row, col),unmarked=True):
                    self.open(_cell[0],_cell[1])
            return True

        return False


    def _num_flagged(self) -> int:
        """Gets the number of cells that have been flagged as potentially mined

        Returns:
            int: number of mines
        """
        return len(list(filter(lambda cell: self._board[cell].is_flagged(), self._board_cells)))


    def complete(self) -> bool:
        """Returns whether or not the board as been completed

        Returns:
            bool: All cells are open or flagged
        """
        return len(self._board_cells) == (self._num_flagged() +
                   len(list(filter(lambda cell: self._board[cell].is_open(), self._board_cells))))


    def is_cell(self, row: str, col: str) -> bool:
        """Checks if the specified cell coordinates are a valid cell in the game
        Args:
            row (str) : row coordinate
            col (str) : column coordinate

        Returns:
            bool: Cell is on the board
        """
        return (row, col) in self._board_cells


    def flag(self, row: str, col: str):
        """Flag a cell as likely to have a mine

        Args:
            row (str): row coordinate
            col (str): column coordinate
        """
        self._board[(row, col)].toggle()


    def reveal(self):
        """Reveal the full map.

        Note:
            There is no need to iterate using items() because we are only interested in the key, not the value.
        """
        for _cell in self._board.items():
            _cell[1].open()
