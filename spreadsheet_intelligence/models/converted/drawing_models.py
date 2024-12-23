from typing import Optional
from dataclasses import dataclass
from .base_models import BaseDrawingConverted
from spreadsheet_intelligence.models.common.enums import (
    FourDirection,
    ArrowType,
    LineType,
    ShapeType,
)
from spreadsheet_intelligence.models.common.common_data import Color
import matplotlib.pyplot as plt


@dataclass
class Connector(BaseDrawingConverted):
    """
    Represents a connector with arrow and line properties.

    Attributes:
        arrow_type (ArrowType): The type of arrow.
        head_pos (tuple[int, int]): The position of the head.
        tail_pos (tuple[int, int]): The position of the tail.
        line_type (LineType): The type of line.
        line_color (Color): The color of the line.
        line_width (int): The width of the line.
        head_type (str): The type of head.
        tail_type (str): The type of tail.
    """
    arrow_type: ArrowType
    head_pos: tuple[int, int]
    tail_pos: tuple[int, int]
    line_type: LineType
    line_color: Color
    line_width: int
    head_type: str
    tail_type: str

    def plot(self, ax: plt.Axes) -> None:
        """
        Plots a simple line representing the connector on the given axes.

        Args:
            ax (plt.Axes): The axes object where the connector will be plotted.

        Note:
            This method currently plots a simple line without considering arrow types or line styles.
            Future implementation will include these features once the design specifications are finalized.
        """
        ax.plot(
            [self.head_pos[0], self.tail_pos[0]],
            [self.head_pos[1], self.tail_pos[1]],
        )


@dataclass
class StraightConnector1(Connector):
    """
    Represents a straight connector, inheriting from Connector.
    """
    pass


@dataclass
class BentConnector3(Connector):
    """
    Represents a bent connector with additional direction properties.
    """
    head_direction: FourDirection
    tail_direction: FourDirection

    def plot(self, ax: plt.Axes) -> None:
        """
        Plots a bent connector with additional features like direction arrows and IDs.
        
        Args:
            ax (plt.Axes): The axes object where the connector will be plotted.
        
        Note:
            This method currently plots a simple line without considering arrow types or line styles.
            Future implementation will include these features once the design specifications are finalized.
        """
        # Plotting a bent connector (temporary example)
        ax.plot(
            [self.head_pos[0], self.tail_pos[0]],
            [self.head_pos[1], self.tail_pos[1]],
            linestyle="--",  # Temporary style
        )
        # Displaying drawing_id
        ax.text(
            self.head_pos[0],
            self.head_pos[1],
            f"{self.drawing_id}",
            fontsize=8,
            color="red",
        )
        # Displaying raw_id
        ax.text(
            self.head_pos[0],
            self.head_pos[1] - 0.1,
            f"{self.raw_id}",
            fontsize=8,
            color="blue",
        )
        # Drawing arrowheads
        self._plot_arrow(ax, self.head_pos, self.head_direction, "head")
        self._plot_arrow(ax, self.tail_pos, self.tail_direction, "tail")

    def _plot_arrow(self, ax: plt.Axes, position: tuple[int, int], direction: FourDirection, t: str) -> None:
        """
        Plots an arrow at the given position and direction.

        Args:
            ax (plt.Axes): The axes object where the arrow will be plotted.
            position (tuple[int, int]): The coordinates of the arrow's base.
            direction (FourDirection): The direction of the arrow.
            t (str): The type of arrow ('head' or 'tail').
        
        Note:
            This method currently plots a simple arrow without considering arrow types or line styles.
            Future implementation will include these features once the design specifications are finalized.
        """
        if t == "head":
            color = "blue"
        else:
            color = "red"
        dx, dy = 0, 0
        if direction == FourDirection.UP:
            dy = -0.1
        elif direction == FourDirection.DOWN:
            dy = 0.1
        elif direction == FourDirection.LEFT:
            dx = -0.1
        elif direction == FourDirection.RIGHT:
            dx = 0.1
        ax.arrow(
            position[0],
            position[1],
            dx,
            dy,
            head_width=0.3,
            head_length=0.3,
            fc=color,
            ec=color,
        )


@dataclass
class Text:
    """
    Represents a text element with optional styling properties.
    """
    content: str
    font_color: Optional[Color]
    font_size: Optional[int]
    alignment: Optional[str]

    def plot(self, x: int, y: int, ax: plt.Axes) -> None:
        """
        Plots the text at the given coordinates on the axes.

        Args:
            x (int): The x-coordinate for the text position.
            y (int): The y-coordinate for the text position.
            ax (plt.Axes): The axes object where the text will be plotted.
        """
        # Plotting the text
        ax.text(x, y, self.content, fontsize=self.font_size)


@dataclass
class Shape(BaseDrawingConverted):
    """
    Represents a shape with properties for type, color, and dimensions.
    """
    shape_type: ShapeType
    fill_color: Optional[Color] # Text boxes may have fill_color as None
    border_color: Optional[Color] # Text boxes may have border_color as None
    x: int
    y: int
    width: int
    height: int
    text: Optional[Text]  # Adapt to list for inline formatting

    def plot(self, ax: plt.Axes) -> None:
        """
        Plots a simple rectangle representing the shape on the given axes.
        
        Args:
            ax (plt.Axes): The axes object where the shape will be plotted.

        Note:
            This method currently plots a simple rectangle without considering fill color or border color.
            Future implementation will include these features once the design specifications are finalized.
        """
        # Plotting a simple rectangle
        ax.add_patch(
            plt.Rectangle(
                (self.x, self.y),
                self.width,
                self.height,
                edgecolor="black",
                facecolor="none",
                # edgecolor=self.border_color.to_hex() if self.border_color else 'none',
                # facecolor=self.fill_color.to_hex() if self.fill_color else 'none'
            )
        )
        if self.text:
            self.text.plot(self.x + self.width / 2, self.y + self.height / 2, ax)
