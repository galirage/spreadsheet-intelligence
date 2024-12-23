from typing import Optional
from spreadsheet_intelligence.converters.drawing.drawing_raw_converters.base_drawing_raw_converter import (
    BaseDrawingConverter,
)
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ShapeAnchorRaw,
    ShapeRaw,
)
from spreadsheet_intelligence.models.raw.theme.theme_models import Theme
from spreadsheet_intelligence.models.common.enums import ShapeType
from spreadsheet_intelligence.utils.helpers import emu_to_cm
from spreadsheet_intelligence.models.converted.drawing_models import Text, Shape


class ShapeConverter(BaseDrawingConverter):
    """
    Converter for shape drawings.

    Attributes:
        anchor (Anchor): The anchor point of the shape.
        drawing (ShapeRaw): The raw shape data.
        theme (Theme): The theme applied to the shape.
        id_counter (int): A counter for generating unique IDs.
    
    TODO:
    - Text parsing is not implemented when the text contains multiple formats.
    """

    def __init__(
        self, shape_anchor_raw: ShapeAnchorRaw, theme: Theme, id_counter: int
    ) -> None:
        """
        Initializes the ShapeConverter with the given shape anchor, theme, and ID counter.

        Args:
            shape_anchor_raw (ShapeAnchorRaw): The raw shape anchor data.
            theme (Theme): The theme to be applied to the shape.
            id_counter (int): A counter for generating unique IDs.
        """
        self.anchor = shape_anchor_raw.anchor
        self.drawing: ShapeRaw = shape_anchor_raw.drawing
        self.theme = theme
        self.id_counter = id_counter

    def extract_shape_type(self) -> ShapeType:
        """
        Extracts the shape type from the raw drawing data.

        Returns:
            ShapeType: The type of the shape.

        Raises:
            ValueError: If the shape type is invalid.
        """
        shape_type_map = {
            "rect": ShapeType.RECT,
            "roundRect": ShapeType.ROUND_RECT,
        }
        try:
            return shape_type_map[self.drawing.shape_type]
        except KeyError:
            raise ValueError(f"Invalid shape type: {self.drawing.shape_type}")

    def convert_unit(self, raw_unit: int) -> float:
        """
        Converts a raw unit to centimeters.

        Args:
            raw_unit (int): The raw unit to be converted.

        Returns:
            float: The converted unit in centimeters.

        TODO: Allow unit conversion method to be specified globally in settings.
        """
        return emu_to_cm(raw_unit)

    def calc_shape_bbox(self) -> tuple:
        """
        Calculates the bounding box of the shape after unit conversion.

        Returns:
            tuple: A tuple containing the x, y coordinates and width, height of the shape.
        """
        drw = self.drawing

        # Convert coordinates and size units
        x = self.convert_unit(drw.x)
        y = self.convert_unit(drw.y)
        width = self.convert_unit(drw.width)
        height = self.convert_unit(drw.height)

        # Perform scale transformation if necessary

        return x, y, width, height

    def convert(self) -> Shape:
        """
        Converts the raw shape data into a Shape object.

        Returns:
            Shape: The converted shape object.
        """
        shape_type = self.extract_shape_type()
        x, y, width, height = self.calc_shape_bbox()
        if self.drawing.style_refs is None:
            fill_color = None
            border_color = None
        else:
            fill_color = self._convert_one_color(
                self.drawing.fill_scheme_clr,
                self.drawing.fill_srgb_clr,
                self.drawing.style_refs.fill_ref,
                self.theme,
            )
            border_color = self._convert_one_color(
                self.drawing.line_scheme_clr,
                self.drawing.line_srgb_clr,
                self.drawing.style_refs.ln_ref,
                self.theme,
            )
        text_data = self.drawing.text_data
        try:
            # TODO: Extract font information and other details when text information becomes more detailed
            text = Text(
                content=text_data[0],
                font_color=None,
                font_size=None,
                alignment=None,
            )
        except IndexError:
            text = None

        return Shape(
            raw_id=self.drawing.id,
            name=self.drawing.name,
            drawing_id=self.id_counter,
            shape_type=shape_type,
            x=x,
            y=y,
            width=width,
            height=height,
            fill_color=fill_color,
            border_color=border_color,
            text=text,
        )
