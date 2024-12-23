from enum import Enum


class FourDirection(Enum):
    """Enum representing four cardinal directions."""
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __str__(self):
        """Return the lowercase name of the direction."""
        return self.name.lower()

    def flip(self):
        """Flip the direction to its opposite."""
        if self == FourDirection.UP:
            return FourDirection.DOWN
        elif self == FourDirection.DOWN:
            return FourDirection.UP
        elif self == FourDirection.LEFT:
            return FourDirection.RIGHT
        elif self == FourDirection.RIGHT:
            return FourDirection.LEFT
        else:
            raise ValueError("Invalid four direction")

    def flip_h(self, rotation: int):
        """
        Flip the direction horizontally based on the rotation.
        
        Args:
            rotation (int): The rotation angle in degrees.
        
        Returns:
            FourDirection: The flipped direction.
        """
        if rotation // 90 % 2 == 0:
            if self in [FourDirection.RIGHT, FourDirection.LEFT]:
                return self.flip()
            else:
                return self
        else:
            if self in [FourDirection.UP, FourDirection.DOWN]:
                return self.flip()
            else:
                return self

    def flip_v(self, rotation: int):
        """
        Flip the direction vertically based on the rotation.
        
        Args:
            rotation (int): The rotation angle in degrees.
        
        Returns:
            FourDirection: The flipped direction.
        """
        if rotation // 90 % 2 == 0:
            if self in [FourDirection.UP, FourDirection.DOWN]:
                return self.flip()
            else:
                return self
        else:
            if self in [FourDirection.RIGHT, FourDirection.LEFT]:
                return self.flip()
            else:
                return self

    def rotate(self, num_of_ninty: int):
        """
        Rotate the direction by a multiple of 90 degrees.
        
        Args:
            num_of_ninty (int): The number of 90-degree rotations.
        
        Returns:
            FourDirection: The rotated direction.
        """
        num_of_ninty = num_of_ninty % 4
        return FourDirection((self.value + num_of_ninty) % 4)

    def i_rotate(self, num_of_ninty: int):
        """
        Rotate the direction inversely by a multiple of 90 degrees.
        
        Args:
            num_of_ninty (int): The number of 90-degree rotations.
        
        Returns:
            FourDirection: The inversely rotated direction.
        """
        num_of_ninty = num_of_ninty % 4
        return self.rotate(4 - num_of_ninty)


class ConnectorType(Enum):
    """Enum representing types of connectors."""
    BENT_CONNECTOR_3 = 1
    STRAIGHT_CONNECTOR_1 = 2

    def __str__(self):
        """Return the lowercase name of the connector type."""
        return self.name.lower()


class ShapeType(Enum):
    """Enum representing types of shapes."""
    RECT = 1
    ROUND_RECT = 2

    def __str__(self):
        """Return the lowercase name of the shape type."""
        return self.name.lower()


class ArrowType(Enum):
    """Enum representing types of arrows."""
    BIDIRECTIONAL = 0
    UNIDIRECTIONAL = 1
    NONE = 2

    def __str__(self):
        """Return the lowercase name of the arrow type."""
        return self.name.lower()


class LineType(Enum):
    """Enum representing types of line styles."""
    SOLID = 0  # none
    DASH = 1  # dash
    SYS_DOT = 2  # sysDot
    SYS_DASH = 3  # sysDash
    DASH_DOT = 4  # dashDot
    LG_DASH = 5  # lgDash
    LG_DASH_DOT = 6  # lgDashDot
    LG_DASH_DOT_DOT = 7  # lgDashDotDot

    def __str__(self):
        """Return the lowercase name of the line type."""
        return self.name.lower()
