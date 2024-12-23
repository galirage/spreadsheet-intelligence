from typing import Optional


class Color:
    """
    Represents a color with RGBA values.

    Attributes:
        hex_code (str): The hexadecimal color code.
        r (int): The red component of the color.
        g (int): The green component of the color.
        b (int): The blue component of the color.
        alpha (float): The alpha component of the color.
    """

    def __init__(
        self,
        hex_code: Optional[str] = None,
        r: Optional[int] = None,
        g: Optional[int] = None,
        b: Optional[int] = None,
        alpha: float = 1.0,
    ):
        """
        Initializes the Color class.

        Args:
            hex_code (Optional[str], optional): The hexadecimal color code.
            r (Optional[int], optional): The red component of the color.
            g (Optional[int], optional): The green component of the color.
            b (Optional[int], optional): The blue component of the color.
            alpha (float, optional): The alpha component of the color.

        Raises:
            ValueError: If the hex_code or r, g, b values are not provided.
        """
        if hex_code:
            self.hex_code = hex_code.lstrip("#")  # '#'を取り除く
            self.r, self.g, self.b = self._hex_to_rgb(self.hex_code)  # RGB値の計算
        elif r is not None and g is not None and b is not None:
            self.r, self.g, self.b = r, g, b
            self.hex_code = f"{r:02X}{g:02X}{b:02X}"
        else:
            raise ValueError("Either hex_code or r, g, b values must be provided")

        self.alpha = self._validate_alpha(alpha)  # アルファ値の検証と設定

    def _validate_alpha(self, alpha: float) -> float:
        """
        Validates the alpha value and raises an exception if it is out of range.

        Args:
            alpha (float): The alpha value to validate.

        Returns:
            float: The valid alpha value.
        """
        if 0.0 <= alpha <= 1.0:
            return alpha
        else:
            raise ValueError("Alpha value must be between 0.0 and 1.0")

    def _hex_to_rgb(self, hex_code: str) -> tuple:
        """
        Converts a hexadecimal color code to an RGB tuple.

        Args:
            hex_code (str): The hexadecimal color code.

        Returns:
            tuple: The RGB tuple.

        Raises:
            ValueError: If the hex_code is not 6 characters long.
        """
        if len(hex_code) != 6:
            raise ValueError("Hex color code must be 6 characters long")
        try:
            r = int(hex_code[0:2], 16)
            g = int(hex_code[2:4], 16)
            b = int(hex_code[4:6], 16)
            return r, g, b
        except ValueError:
            raise ValueError("Invalid hex color code")

    def to_rgba(self) -> tuple:
        """
        Returns the RGBA tuple.

        Returns:
            tuple: The RGBA tuple.
        """
        return self.r, self.g, self.b, self.alpha

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f"Color(RGBA=({self.r}, {self.g}, {self.b}, {self.alpha}))"

    def adjust_color(
        self, lum_mod: Optional[int], lum_off: Optional[int], shade: Optional[int]
    ) -> "Color":
        """
        Adjusts the color based on the given parameters.

        Args:
            lum_mod (Optional[int]): The luminance adjustment value.
            lum_off (Optional[int]): The luminance adjustment value.
            shade (Optional[int]): The hue adjustment value.

        Returns:
            str: The adjusted 16-bit color code.
        """
        # Convert the 16-bit color code to RGB
        r = int(self.hex_code[0:2], 16)
        g = int(self.hex_code[2:4], 16)
        b = int(self.hex_code[4:6], 16)

        # Apply lum_mod
        if lum_mod is not None:
            r = int(r * (lum_mod / 100000))
            g = int(g * (lum_mod / 100000))
            b = int(b * (lum_mod / 100000))

        # Apply lum_off
        if lum_off is not None:
            r = r + int((lum_off / 100000) * 255)
            g = g + int((lum_off / 100000) * 255)
            b = b + int((lum_off / 100000) * 255)

        # Apply shade
        if shade is not None:
            r = int(r * shade / 100000)
            g = int(g * shade / 100000)
            b = int(b * shade / 100000)

        # Clipping values
        r = min(max(0, int(r)), 255)
        g = min(max(0, int(g)), 255)
        b = min(max(0, int(b)), 255)

        # Generate a new color code
        return Color(f"{r:02X}{g:02X}{b:02X}")
