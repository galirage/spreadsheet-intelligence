from typing import Optional, Union
from abc import ABC, abstractmethod
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ShapeAnchorRaw,
    ConnectorAnchorRaw,
)
from spreadsheet_intelligence.models.raw.drawing.base_models import BaseDrawingRaw
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    SchemeClr,
    SrgbClr,
    StyleBaseRef,
)
from spreadsheet_intelligence.models.common.common_data import Color
from spreadsheet_intelligence.models.raw.theme.theme_models import Theme


class BaseDrawingConverter(ABC):
    """
    Base abstract class for drawing converters.

    Attributes:
        anchor (Anchor): The anchor point of the drawing.
        drawing (BaseDrawingRaw): The raw drawing data.
        refined (Optional[BaseDrawingRaw]): The refined drawing data after conversion.
    """
    def __init__(self, raw: Union[ShapeAnchorRaw, ConnectorAnchorRaw]):
        """Initializes the BaseDrawingConverter with raw drawing data.

        Args:
            raw (Union[ShapeAnchorRaw, ConnectorAnchorRaw]): The raw drawing data.
        """
        self.anchor = raw.anchor
        self.drawing = raw.drawing
        self.refined = None

        self._validate_drawing(self.drawing)

    @staticmethod
    def _convert_one_color(
        scheme_clr: Optional[SchemeClr],
        srgb_clr: Optional[SrgbClr],
        style_base_ref: StyleBaseRef,
        theme: Theme,
    ) -> Color:
        """Converts color information to a Color object.

        Args:
            scheme_clr (Optional[SchemeClr]): The scheme color.
            srgb_clr (Optional[SrgbClr]): The sRGB color.
            style_base_ref (StyleBaseRef): The style base reference.
            theme (Theme): The theme used for color conversion.

        Returns:
            Color: The converted color object.

        Raises:
            ValueError: If the color type is invalid.
        """
        if scheme_clr is not None:
            return scheme_clr.get_color(theme)
        elif srgb_clr is not None:
            return srgb_clr.val
        else:
            ref_clr = style_base_ref.ref_clr
            if isinstance(ref_clr, SchemeClr):
                return ref_clr.get_color(theme)
            elif isinstance(ref_clr, SrgbClr):
                return ref_clr.val
            else:
                raise ValueError(f"Invalid color type: {type(style_base_ref)}")

    def _validate_drawing(self, drawing: BaseDrawingRaw):
        """Validates if the drawing is the expected input for the converter.

        Args:
            drawing (BaseDrawingRaw): The drawing to validate.

        Returns:
            bool: True if the drawing is valid, False otherwise.
        """
        return True

    @abstractmethod
    def convert(self):
        """Abstract method to convert the drawing.

        This method should be implemented by subclasses.
        """
        pass
