import os
import random

from cell import GameCell

class GameBoard:
    """Game board class.
    
    """
    _min_mines = 1 # ( _r_size - 1 ) * ( _c_size - 1 )
    _max_mines = 3 # ( _r_size * _c_size ) - 1
    _coord_list = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _board_cells = []
    _mine_cells = []
    _board = {}

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
        _display += "".join([ " " + c for c in self._coord_list[:self.c_size] ])
        _display += "\n"
        _display += " /" + "-" * ((self.c_size * 2)) + "\\"
        _display += "   Mines Left: " + str(self.mines_left - self._num_flagged()) + "\n"
        for r in self._coord_list[:self.r_size]:
            _display += r + "|"
            for c in self._coord_list[:self.c_size]:
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
        if 1 < size <= self._max_r:
            self._r_size = size
        else:
            raise ValueError("Board width must be between 2 and " + str(self._max_r) + " cells.")


    @property
    def c_size(self) -> int:
        """(property) Get the size in columns of the board

        Returns:
            int: number of columns
        """
        return self._c_size
    

    @c_size.setter
    def c_size(self, size: int):
        """Set the Y dimension

        Args:
            size (int): number of columns

        Raises:
            ValueError: Given size is outside the bounds
        """
        if 1 < size <= self._max_c:
            self._c_size = size
        else:
            raise ValueError("Board height must be between 2 and " + str(self._max_c) + " cells")


    def _create_board(self):
        """Creates the board
        """
        self._board_cells = [ (r,c) for r in self._coord_list[:self.r_size] for c in self._coord_list[:self.c_size] ]
        self._mine_cells = random.sample(self._board_cells, self.mines_left)
        for _cell in self._board_cells:
            if _cell in self._mine_cells:
                self._board[_cell] = GameCell(name="M",mine=True)
            else:
                _neighbor_mines = list(filter(lambda cell: cell in self._mine_cells, self._get_neighbors(_cell)))
                self._board[_cell] = GameCell(name=str(len(_neighbor_mines)),mine=False)


    def _get_neighbors(self,_cell):
        """Get the neighboring cells in the board
           based on https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list
        """
        _cell_r = self._coord_list.index(_cell[0])
        _cell_c = self._coord_list.index(_cell[1])
        return [(self._coord_list[r2],self._coord_list[c2]) for r2 in range(_cell_r-1,_cell_r+2) for c2 in range(_cell_c-1,_cell_c+2)
                                    if ((_cell_r != r2 or _cell_c != c2) and
                                        (0 <= r2 <= self.r_size - 1) and
                                        (0 <= c2 <= self.c_size - 1)
                                        )]


    def open(self, row: str, col: str) -> bool:
        """Open (possibly recursively) a cell

        Args:
            row (str): row coordinate
            col (str): column coordinate
        
        Returns:
            bool: Whether the game is still going
        """
        if not self._board[(row, col)].open():
            if self._board[(row, col)].is_safe():
                for cell in list(filter(lambda cell: not self._board[cell].is_open(), self._get_neighbors((row, col)))):
                    self.open(cell[0],cell[1])
            return True
        else:
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
        return len(self._board_cells) == (self._num_flagged() + len(list(filter(lambda cell: self._board[cell].is_open(), self._board_cells))))
    

    def is_cell(self, row: str, col: str):
        return (row, col) in self._board_cells


    def flag(self, row: str, col: str):
        """Flag a cell as likely to have a mine

        Args:
            row (str): row coordinate
            col (str): column coordinate
        """
        self._board[(row, col)].toggle()


    def reveal(self):
        """Reveal the full map
        """
        for _cell in self._board.keys():
            self._board[_cell].open()

