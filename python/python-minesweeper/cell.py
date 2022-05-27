from colorama import Fore, Back, Style
import emoji

class GameCell:
    """Gameboard cell. May or may not be a mine.
    """
    _is_flagged = False
    _is_open = False

    def __init__(self, name: int, mine=False):
        self.is_mine = mine
        self.label = name 

    def __repr__(self):
        if self._is_flagged:
            return Back.WHITE + Style.DIM + emoji.emojize(":triangular_flag:") + Style.RESET_ALL
        else:
            return self.label()


    @property
    def label(self) -> str:
        """Returns the label of the cell.

        Returns:
            str: M => Mine. If you see this, the game is over.
                 # => Number of adjacent mines.
        """
        return self._label


    @label.setter
    def label(self, name: int):
        """Sets the label for the cell

        Args:
            name (str): Label string
        """
        if self.is_mine:
            self._label = Style.BRIGHT + Back.RED + emoji.emojize(":bomb:") + Style.RESET_ALL
        else:
            color = ""
            if name == 0:
                name = " "
            elif name == 1:
                color = Style.BRIGHT + Fore.GREEN
            elif name == 2:
                color = Style.NORMAL + Fore.GREEN
            elif name == 3:
                color = Fore.GREEN
            elif name == 4:
                color = Style.BRIGHT + Fore.BLUE
            elif name == 5:
                color = Style.NORMAL + Fore.BLUE
            elif name == 6:
                color = Fore.BLUE
            elif name == 7:
                color = Fore.RED
            elif name == 8:
                color = Style.BRIGHT + Fore.RED
            self._label = Style.DIM + Back.BLACK + color + str(name) + Style.RESET_ALL


    @property
    def is_mine(self):
        """Returns whether this cell contains a mine

        Returns:
            bool: True/False about whether the cell is a mine
        """
        return self._is_mine


    @is_mine.setter
    def is_mine(self, mine):
        """Sets up the cell to be a mine... or not

        Args:
            mine (bool): Is this a mine?
        """
        self._is_mine = mine


    def toggle(self):
        """Toggle whether the cell is flagged. This is used when opening areas
        """
        if not self._is_flagged:
            self._is_flagged = True
            self.label = "F"
        else:
            self._is_flagged = False


    def open(self) -> bool:
        """Open the cell

        Returns:
            bool: Whether or not you opened a mine.
        """
        self._is_open = True
        return self.is_mine

if __name__ == "__main__":
    c = GameCell(name=0,mine=True)
    print(c.label)
