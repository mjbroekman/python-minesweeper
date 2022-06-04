"""GameCell class

Author:
    Maarten Broekman - https://github.com/mjbroekman

Raises:
    ValueError if there are an impossible number of adjacent mines (more than 8)

Returns:
    a Gamecell object
"""
from colorama import Back, Style
import emoji

class GameCell:
    """Gameboard cell. May or may not be a mine.
    """
    _is_flagged = False
    _is_open = False
    _int_name = 0

    def __init__(self, name, mine=False):
        """Constructor

        Args:
            name: value to set the label to (number of neighbor mines or M if we are a mine)
            mine (bool, optional): Are we a mine? Defaults to False.
        """
        self.is_mine = mine
        try:
            self.label = name 
        except ValueError as e:
            exit(e)


    def __repr__(self):
        """Representation matters

        Returns:
            str: String representation of the cell
        """
        if self._is_flagged:
            return Style.DIM + Back.CYAN + emoji.emojize(":play_button:") + " " + Style.RESET_ALL
        elif self._is_open:
            return Style.DIM + Back.CYAN + self.label + Style.RESET_ALL
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
    def label(self, name: str):
        """Sets the label for the cell

        Args:
            name (str): Label string
        """
        if self.is_mine:
            self._int_name = -1
            self._label = Style.BRIGHT + Back.RED + emoji.emojize(":bomb:") + Style.RESET_ALL
        else:
            self._int_name = int(name)
            if int(name) == 0:
                name = emoji.emojize(":black_square_button:")
            elif 0 < int(name) < 9:
                name = emoji.emojize(":keycap_" + name + ":") + " "
            else:
                raise ValueError("Impossible number of adjacent mines. Must be between 0 and 9 exclusive.")

            self._label = name


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


    def is_flagged(self):
        """Returns whether we have been flagged as a mine or not
        """
        return self._is_flagged

    def is_open(self) -> bool:
        """Have we been opened already. Used for filtering neighbor cells.

        Returns:
            bool: self._is_open
        """
        return self._is_open


    def is_safe(self) -> bool:
        """Are we completely safe? i.e. Are we empty and have no mines in any neighboring cell?

        Returns:
            bool: True if we have no neighboring cells containing a mine, False otherwise.
        """
        if self._int_name == 0:
            return True
        return False


    def toggle(self):
        """Toggle whether the cell is flagged. This is used when opening areas
        """
        if not self._is_flagged:
            self._is_flagged = True
        else:
            self._is_flagged = False


    def open(self) -> bool:
        """Open the cell.

        Returns:
            bool: Whether or not you opened a mine.
        """
        self._is_open = True
        self._is_flagged = False
        return self.is_mine
