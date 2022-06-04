import os
import sys

try:
    import _tkinter        
except ModuleNotFoundError:
    if 'homebrew' in str(os.path):
        if os.path.exists('/opt/homebrew/Cellar/python-tk@3.9'):
            for version in os.listdir('/opt/homebrew/Cellar/python-tk@3.9'):
                if os.path.exists('/opt/homebrew/Cellar/python-tk@3.9/' + version + '/libexec'):
                    sys.path.insert(0,'/opt/homebrew/Cellar/python-tk@3.9/' + version + '/libexec')

            import _tkinter
        else:
            exit('Unable to find a valid module: _tkinter or tkinter')
    else:
        exit('Open a PR to add the appropriate paths for Tk')

try:
    import tkinter as tk
except ModuleNotFoundError as e:
    exit('Unable to import a working tkinter...\n' + str(e))

from board import GameBoard

class GameBoardTk(GameBoard, tk.Frame):
    _screen = None
    _root = None

    def __init__(self, r_size: int, c_size: int, num_mines=-1):
        """Create the game board

        Args:
            r_size (int): Horizontal size
            c_size (int): Vertical size
            num_mines (int, optional): Number of mines. Defaults to -1 (random).
        """
        self._get_screen_size()
        self.r_size = r_size
        self.c_size = c_size
        self.mines_left = num_mines
        self._create_board()

    def _get_screen_size(self):
        """Gets the screen size and converts it to the maximum number of rows and columns
        """
        try:
            _tmp = tk.Tk(baseName="PySweeper")
        except Exception as e:
            exit('Got an exception ' + str(e))

        self._max_r = int(_tmp.winfo_screenmmheight() / 5) - 3
        self._max_c = int(_tmp.winfo_screenmmwidth() / 5) - 5
        _tmp.destroy()

    def _create_board(self,master=None):
        """Initialize the backend gameboard
        """
        self._root = tk.Tk(baseName="PySweeper")
        tk.Frame.__init__(self._root)
        super()._create_board()
    

    def _init_cell(self, name, mine: bool):
        pass