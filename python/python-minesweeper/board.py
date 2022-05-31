import os
import random

from cell import GameCell

class GameBoard:
    """Game board class.
    
    """
    _min_mines = 1 # ( _x_size - 1 ) * ( _y_size - 1 )
    _max_mines = 3 # ( _x_size * _y_size ) - 1
    _coord_list = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _board = []

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
        return self._mines_left
    
    @mines_left.setter
    def mines_left(self, mines: int):
        if mines < 1:
            mines = random.randrange(1, (self.x_size * self.y_size))

        if mines > ((self.x_size * self.y_size) - 1):
            raise ValueError("Too many mines to fit. Must be between 1 and " + str((self.x_size * self.y_size) - 1))

        self._mines_left = mines

    @property
    def x_size(self) -> int:
        return self._x_size
    
    @x_size.setter
    def x_size(self, size: int):
        if 1 < size <= self._max_x:
            self._x_size = size
        else:
            raise ValueError("Board width must be between 2 and " + str(self._max_x) + " cells.")

    @property
    def y_size(self) -> int:
        return self._y_size
    
    @y_size.setter
    def y_size(self, size: int):
        if 1 < size <= self._max_y:
            self._y_size = size
        else:
            raise ValueError("Board height must be between 2 and " + str(self._max_y) + " cells")

    def _create_board(self):
        """Creates the board
        """
        _board_cells = [ (x,y) for x in self._coord_list[:self.x_size] for y in self._coord_list[:self.y_size] ]
        _mine_cells = random.sample(_board_cells, self.mines_left)
        for _cell in _board_cells:
            if _cell in _mine_cells:
                self._board[_cell] = GameCell(name="M",mine=True)
            else:
                _cell_x = self._coord_list.index(_cell[0])
                _cell_y = self._coord_list.index(_cell[1])
                # based on https://stackoverflow.com/questions/1620940/determining-neighbours-of-cell-two-dimensional-list
                _neighbor_mines = [(self._coord_list[x2],self._coord_list[y2]) for x2 in range(_cell_x-1,_cell_x+2) for y2 in range(_cell_y-1,_cell_y+2)
                                    if ((_cell_x != x2 or _cell_y != y2) and
                                        (0 <= x2 <= self.x_size) and
                                        (0 <= y2 <= self.y_size) and
                                        (self._coord_list[x2],self._coord_list[y2]) in _mine_cells
                                        )]
                self._board[_cell] = GameCell(name=str(len(_neighbor_mines)),mine=False)

