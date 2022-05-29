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
            return Style.DIM + Back.CYAN + emoji.emojize(":play_button:") + Style.RESET_ALL
        elif self._is_open:
            return Style.DIM + Back.CYAN + self.label
        else:
            return Style.DIM + Back.CYAN + emoji.emojize(":blue_square:") + Style.RESET_ALL

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
                name = emoji.emojize(":black_square_button:")
            elif 0 < name < 9:
                name = emoji.emojize(":keycap_" + str(name) + ":")
            else:
                raise ValueError("Impossible number of adjacent mines. Must be between 0 and 9 exclusive.")

            self._label = Style.DIM + Back.BLUE + color + str(name) + Style.RESET_ALL


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
        else:
            self._is_flagged = False


    def open(self) -> bool:
        """Open the cell

        Returns:
            bool: Whether or not you opened a mine.
        """
        self._is_open = True
        self._is_flagged = False
        return self.is_mine

if __name__ == "__main__":
    c = GameCell(name=0,mine=True)
    print(c)
    c.toggle()
    print(c)
    boom = c.open()
    print(c)
    c = GameCell(name=8)
    print(c)
    c.toggle()
    print(c)
    boom = c.open()
    print(c)
