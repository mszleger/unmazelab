'''A module containing classes representing different types of vectors.'''

class Vector2D:
    '''2D vector with atributes (x, y).

    Attributes:
        x: X position of vector.
        y: Y position of vector.
    '''

    def __init__(self, x: int, y: int):
        '''Initializes values of vector.

        Args:
            x: X position of vector.
            y: Y position of vector.
        '''
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        '''X position of vector.'''
        return self._x

    @x.setter
    def x(self, x: int):
        '''Setter of x value of vector.

        Args:
            x: X position of vector.

        Raises:
            ValueError: If x isn't of type int.
        '''
        if not isinstance(x, int):
            raise ValueError('X has to be value of type int')
        self._x = x

    @property
    def y(self) -> int:
        '''Y position of vector.'''
        return self._y

    @y.setter
    def y(self, y: int):
        '''Setter of y value of vector.

        Args:
            y: Y position of vector.

        Raises:
            ValueError: If y isn't of type int.
        '''
        if not isinstance(y, int):
            raise ValueError('Y has to be value of type int')
        self._y = y

    def __repr__(self):
        '''Returns representation string of vector.

        Returns:
            String representation of vector in form of (x, y). Fox example:

            (5, 8)
        '''
        return f'({self.x}, {self.y})'
