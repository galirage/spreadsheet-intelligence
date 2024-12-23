import xml.etree.ElementTree as ET
from .base_drawing_parser import BaseDrawingParser
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    PictureRaw,
    PictureAnchorRaw,
)
from spreadsheet_intelligence.models.raw.drawing.anchor_models import Anchor


class PictureParser(BaseDrawingParser):
    def _parse_drawing(self, element: ET.Element) -> PictureRaw:
        """Parses the drawing element and returns a PictureRaw object.

        Args:
            element (ET.Element): The drawing element.

        Returns:
            PictureRaw: The parsed PictureRaw object.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    def _create_anchor_raw(
        self, anchor: Anchor, drawing_raw: PictureRaw
    ) -> PictureAnchorRaw:
        """Creates a PictureAnchorRaw object.

        Args:
            anchor (Anchor): The anchor object.
            drawing_raw (PictureRaw): The drawing raw object.

        Returns:
            PictureAnchorRaw: The created PictureAnchorRaw object.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError
