class Vector2D:
    """
    A class to represent a 2D vector.

    Attributes:
        x (int): X position of vector.
        y (int): Y position of vector.
    """
    def __init__(self, x, y):
        """
        Initialize values of vector.

        :param x: X position of vector.
        :type x: int
        :param y: Y position of vector.
        :type y: int
        """
        self.x = x
        self.y = y

    @property
    def x(self):
        """
        Getter of x value of vector.

        :return: X position of vector.
        :rtype: int
        """
        return self._x

    @x.setter
    def x(self, x):
        """
        Setter of x value of vector.

        :param x: X position of vector.
        :type x: int

        :raises ValueError: If x isn't of type int.
        """
        if type(x) != int:
            raise ValueError("X has to be value of type int")
        self._x = x

    @property
    def y(self):
        """
        Getter of y value of vector.

        :return: Y position of vector.
        :rtype: int
        """
        return self._y

    @y.setter
    def y(self, y):
        """
        Setter of y value of vector.

        :param y: Y position of vector.
        :type y: int

        :raises ValueError: If y isn't of type int.
        """
        if type(y) != int:
            raise ValueError("Y has to be value of type int")
        self._y = y

    def __str__(self):
        """
        Dunder returning string representation of vector.

        :return: String representation of vector.
        :rtype: str
        """
        return f'({self.x}, {self.y})'

    def __repr__(self):
        """
        Dunder returning string representation of vector.

        :return: String representation of vector.
        :rtype: str
        """
        return f'({self.x}, {self.y})'