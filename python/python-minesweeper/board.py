import os
import random

from cell import GameCell

class GameBoard:
    """Game board class.
    
    """
    _min_mines = 1 # ( _x_size - 1 ) * ( _y_size - 1 )
    _max_mines = 3 # ( _x_size * _y_size ) - 1
    _coord_list = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _board_cells = []
    _mine_cells = []
    _board = {}

    def __init__(self, x_size: int, y_size: int, num_mines=-1):
        """Create the game board

        Args:
            x_size (int): Horizontal size
            y_size (int): Vertical size
            num_mines (int, optional): Number of mines. Defaults to -1 (random).
        """
        self._get_term_size()
        self.x_size = x_size
        self.y_size = y_size
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
        if self.x_size > 9:
            _display += " " * int(((self.y_size * 2) - 9) / 2)
        _display += "PySweeper\n"
        _display += "  "
        _display += "".join([ " " + y for y in self._coord_list[:self.y_size] ])
        _display += "\n"
        _display += " /" + "-" * ((self.y_size * 2)) + "\\"
        _display += "   Mines Left: " + str(self.mines_left - self._num_flagged()) + "\n"
        for x in self._coord_list[:self.x_size]:
            _display += x + "|"
            for y in self._coord_list[:self.y_size]:
                _display += str(self._board[(x,y)])
            _display += "|\n"
        _display += " \\" + "-" * ((self.y_size * 2))  + "/\n"
        return _display


    def _get_term_size(self):
        """(private) Get the size of the terminal for boundary checking

        Raises:
            ValueError: if the screen is too narrow or too short
        """
        if os.get_terminal_size()[0] > 46:
            self._max_x = 36
        else:
            self._max_x = os.get_terminal_size()[0] - 10

        if os.get_terminal_size()[1] > 41:
            self._max_y = 36
        else:
            self._max_y = os.get_terminal_size()[1] - 7

        if self._max_x < 0:
            raise ValueError("Screen is too narrow. Minimum screen width is 10 columns.")

        if self._max_y < 0:
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
            mines = random.randrange(1, (self.x_size * self.y_size))

        if mines > ((self.x_size * self.y_size) - 1):
            raise ValueError("Too many mines to fit. Must be between 1 and " + str((self.x_size * self.y_size) - 1))

        self._mines_left = mines


    @property
    def x_size(self) -> int:
        """(property) Get the size in rows of the board

        Returns:
            int: number of rows
        """
        return self._x_size
    

    @x_size.setter
    def x_size(self, size: int):
        """(setter) Set the size in rows of the board

        Args:
            size (int): number of rows

        Raises:
            ValueError: Given size is outside the bounds
        """
        if 1 < size <= self._max_x:
            self._x_size = size
        else:
            raise ValueError("Board width must be between 2 and " + str(self._max_x) + " cells.")


    @property
    def y_size(self) -> int:
        """(property) Get the size in columns of the board

        Returns:
            int: number of columns
        """
        return self._y_size
    

    @y_size.setter
    def y_size(self, size: int):
        """Set the Y dimension

        Args:
            size (int): number of columns

        Raises:
            ValueError: Given size is outside the bounds
        """
        if 1 < size <= self._max_y:
            self._y_size = size
        else:
            raise ValueError("Board height must be between 2 and " + str(self._max_y) + " cells")


    def _create_board(self):
        """Creates the board
        """
        self._board_cells = [ (x,y) for x in self._coord_list[:self.x_size] for y in self._coord_list[:self.y_size] ]
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
        _cell_x = self._coord_list.index(_cell[0])
        _cell_y = self._coord_list.index(_cell[1])
        return [(self._coord_list[x2],self._coord_list[y2]) for x2 in range(_cell_x-1,_cell_x+2) for y2 in range(_cell_y-1,_cell_y+2)
                                    if ((_cell_x != x2 or _cell_y != y2) and
                                        (0 <= x2 <= self.x_size - 1) and
                                        (0 <= y2 <= self.y_size - 1)
                                        )]


    def open(self, x_loc: str, y_loc: str):
        """Open (possibly recursively) a cell

        Args:
            x_loc (str): X coordinate
            y_loc (str): Y coordinate
        """
        if not self._board[(x_loc, y_loc)].open():
            if self._board[(x_loc, y_loc)].is_safe():
                for cell in list(filter(lambda cell: not self._board[cell].is_open(), self._get_neighbors((x_loc, y_loc)))):
                    self.open(cell[0],cell[1])
            print(self)
        else:
            print("Too bad. You hit a mine. Better luck next time.")
            self._reveal()


    def _num_flagged(self) -> int:
        """Gets the number of cells that have been flagged as potentially mined

        Returns:
            int: number of mines
        """
        return len(list(filter(lambda cell: self._board[cell].is_flagged(), self._board_cells)))


    def flag(self, x_loc: str, y_loc: str):
        """Flag a cell as likely to have a mine

        Args:
            x_loc (str): X coordinate
            y_loc (str): Y coordinate
        """
        self._board[(x_loc, y_loc)].toggle()
        print(self)


    def _reveal(self):
        """Reveal the full map
        """
        for _cell in self._board.keys():
            self._board[_cell].open()
        print(self)
