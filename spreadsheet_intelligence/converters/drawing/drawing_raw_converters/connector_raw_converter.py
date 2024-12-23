import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from typing import Optional
from abc import ABC, abstractmethod
from spreadsheet_intelligence.converters.drawing.drawing_raw_converters.base_drawing_raw_converter import (
    BaseDrawingConverter,
)
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ConnectorAnchorRaw,
    ConnectorRaw,
)
from spreadsheet_intelligence.models.converted.drawing_models import (
    StraightConnector1,
    BentConnector3,
)
from spreadsheet_intelligence.utils.helpers import apply_rotation, apply_flip, emu_to_cm
from spreadsheet_intelligence.models.common.enums import FourDirection, ConnectorType
from spreadsheet_intelligence.models.converted.drawing_models import ArrowType, LineType
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    Theme,
)
from spreadsheet_intelligence.models.converted.drawing_models import Connector

class ConnectorConverter(BaseDrawingConverter, ABC):
    """Abstract base class for converting connector drawings.

    Attributes:
        anchor (Anchor): The anchor point of the connector.
        drawing (ConnectorRaw): The raw drawing data of the connector.
        refined (Optional[Connector]): The refined drawing data after conversion.
        theme (Theme): The theme applied to the drawing.
        id_counter (int): A counter for generating unique IDs.
    """

    def __init__(
        self, connector_anchor_raw: ConnectorAnchorRaw, theme: Theme, id_counter: int
    ):
        """Initialize the ConnectorConverter.

        Args:
            connector_anchor_raw (ConnectorAnchorRaw): The raw anchor data of the connector.
            theme (Theme): The theme applied to the drawing.
            id_counter (int): A counter for generating unique IDs.
        """
        self.anchor = connector_anchor_raw.anchor
        self.drawing = connector_anchor_raw.drawing
        self.refined: Optional[Connector] = None
        self.theme = theme
        self.id_counter = id_counter

    def convert_length_unit(self, raw_unit: int) -> float:
        """Converts length from EMU to centimeters.

        Args:
            raw_unit (int): The length in EMU.

        Returns:
            float: The length in centimeters.
        """
        # TODO: Allow unit conversion method to be specified in settings.
        return emu_to_cm(raw_unit)

    def convert_angle_unit(self, raw_unit: int) -> float:
        """Converts angle from raw units to degrees.

        Args:
            raw_unit (int): The angle in raw units.

        Returns:
            float: The angle in degrees.
        """
        # TODO: Allow unit conversion method to be specified in settings.
        return raw_unit / 60000

    def convert_units(self) -> tuple:
        """Converts the drawing's position, size, and rotation units.

        Returns:
            tuple: A tuple containing the converted x, y, width, height, and rotation.
        """
        x = self.convert_length_unit(self.drawing.x)
        y = self.convert_length_unit(self.drawing.y)
        w = self.convert_length_unit(self.drawing.width)
        h = self.convert_length_unit(self.drawing.height)
        rotation = self.convert_angle_unit(self.drawing.rotation)
        return x, y, w, h, rotation

    def calc_endpoints_pos(self, x: float, y: float, w: float, h: float, rotation: float, flip_h: bool, flip_v: bool) -> tuple:
        """Calculates the positions of the connector's endpoints.

        Args:
            x (float): The x-coordinate of the drawing.
            y (float): The y-coordinate of the drawing.
            w (float): The width of the drawing.
            h (float): The height of the drawing.
            rotation (float): The rotation of the drawing.
            flip_h (bool): Whether the drawing is flipped horizontally.
            flip_v (bool): Whether the drawing is flipped vertically.

        Returns:
            tuple: A tuple containing the rotated and flipped head and tail positions.
        """
        head_position = (x, y)
        tail_position = (x + w, y + h)

        # TODO: Apply scale/offset here.

        # Calculate the center of rotation
        center_position = (x + w / 2, y + h / 2)

        # Apply rotation
        r_head = apply_rotation(head_position, center_position, rotation)
        r_tail = apply_rotation(tail_position, center_position, rotation)

        # Apply flip
        r_head = apply_flip(r_head, center_position, flip_h, flip_v)
        r_tail = apply_flip(r_tail, center_position, flip_h, flip_v)
        return r_head, r_tail

    def extract_line_style(self) -> LineType:
        """Extracts the line style from the drawing.

        Returns:
            LineType: The line style as a LineType enum.

        Raises:
            ValueError: If the line style is invalid.
        """
        line_style_map = {
            "none": LineType.SOLID,
            "dash": LineType.DASH,
            "sysDot": LineType.SYS_DOT,
            "sysDash": LineType.SYS_DASH,
            "dashDot": LineType.DASH_DOT,
            "lgDash": LineType.LG_DASH,
            "lgDashDot": LineType.LG_DASH_DOT,
            "lgDashDotDot": LineType.LG_DASH_DOT_DOT,
        }
        try:
            return line_style_map[self.drawing.arrow_line.dash_style]
        except KeyError:
            raise ValueError(
                f"Invalid line style: {self.drawing.arrow_line.dash_style}"
            )

    def extract_arrow_type(self) -> ArrowType:
        """Extracts the arrow type from the drawing.

        Returns:
            ArrowType: The arrow type as an ArrowType enum.

        Raises:
            ValueError: If the arrow type is invalid.
        """
        if (
            self.drawing.arrow_line.head.type == "none"
            and self.drawing.arrow_line.tail.type == "none"
        ):
            return ArrowType.NONE
        elif (
            self.drawing.arrow_line.head.type == "none"
            and self.drawing.arrow_line.tail.type != "none"
        ) or (
            self.drawing.arrow_line.head.type != "none"
            and self.drawing.arrow_line.tail.type == "none"
        ):
            return ArrowType.UNIDIRECTIONAL
        elif (
            self.drawing.arrow_line.head.type != "none"
            and self.drawing.arrow_line.tail.type != "none"
        ):
            return ArrowType.BIDIRECTIONAL
        else:
            raise ValueError(
                f"Invalid arrow type: {self.drawing.arrow_line.head.type} {self.drawing.arrow_line.tail.type}"
            )

    @abstractmethod
    def convert(self):
        """Abstract method to convert the drawing."""
        pass


class StraightConnector1Converter(ConnectorConverter):
    """Converter for StraightConnector1 drawings."""

    def __init__(
        self, connector_anchor_raw: ConnectorAnchorRaw, theme: Theme, id_counter: int
    ):
        self.anchor = connector_anchor_raw.anchor
        self.drawing: ConnectorRaw = connector_anchor_raw.drawing
        self.theme = theme
        self.refined: Optional[StraightConnector1] = None
        self.id_counter = id_counter

    def _validate_drawing(self, drawing: ConnectorRaw):
        """Validates that the drawing is of type StraightConnector1.

        Args:
            drawing: The raw drawing data.

        Raises:
            ValueError: If the drawing type is not StraightConnector1.
        """
        if drawing.connector_type != ConnectorType.STRAIGHT_CONNECTOR_1:
            raise ValueError(
                f"The type must be StraightConnector1. {drawing.connector_type}"
            )

    def convert(self) -> StraightConnector1:
        """Converts the raw drawing to a StraightConnector1 object.

        Returns:
            A StraightConnector1 object.
        """
        x, y, w, h, rotation = self.convert_units()
        head_pos, tail_pos = self.calc_endpoints_pos(
            x, y, w, h, rotation, self.drawing.flip_h, self.drawing.flip_v
        )
        line_type = self.extract_line_style()
        arrow_type = self.extract_arrow_type()
        line_color = self._convert_one_color(
            self.drawing.scheme_clr,
            self.drawing.srgb_clr,
            self.drawing.style_refs.ln_ref,
            self.theme,
        )
        line_width = self.drawing.arrow_line.width
        head_type = self.drawing.arrow_line.head.type
        tail_type = self.drawing.arrow_line.tail.type

        self.refined = StraightConnector1(
            raw_id=self.drawing.id,
            name=self.drawing.name,
            drawing_id=self.id_counter,
            arrow_type=arrow_type,
            line_type=line_type,
            line_color=line_color,
            line_width=line_width,
            head_type=head_type,
            tail_type=tail_type,
            head_pos=head_pos,
            tail_pos=tail_pos,
        )
        return self.refined


class BentConnector3Converter(ConnectorConverter):
    """Converter for BentConnector3 drawings."""

    def __init__(
        self, connector_anchor_raw: ConnectorAnchorRaw, theme: Theme, id_counter: int
    ):
        self.anchor = connector_anchor_raw.anchor
        self.drawing: ConnectorRaw = connector_anchor_raw.drawing
        self.theme = theme
        self.refined: Optional[BentConnector3] = None
        self.id_counter = id_counter
        self.interm_ln_thrd = 1000

    def _validate_drawing(self, drawing: ConnectorRaw):
        """Validates that the drawing is of type BentConnector3 and has a valid rotation.

        Args:
            drawing: The raw drawing data.

        Raises:
            ValueError: If the drawing type is not BentConnector3 or the rotation is invalid.
        """
        if drawing.connector_type != ConnectorType.BENT_CONNECTOR_3:
            raise ValueError(
                f"The type must be BentConnector3. {drawing.connector_type}"
            )
        rot = drawing.rotation
        if rot not in [0 * 60000, 90 * 60000, 180 * 60000, 270 * 60000]:
            raise ValueError(
                "The rotation of BentConnector3 must be either 0, 90, 180, or 270."
            )

    def convert_angle_unit(self, raw_unit: int) -> int:
        """Converts angle from raw units to degrees.

        Args:
            raw_unit: The angle in raw units.

        Returns:
            The angle in degrees.
        """
        # TODO: Allow unit conversion method to be specified in settings.
        return int(raw_unit / 60000)

    def extract_endpoints_direction(self, rotation, flip_h, flip_v, interm_ln_pos):
        """Extracts the directions of the arrowheads at both ends.

        Args:
            rotation: The rotation of the drawing.
            flip_h: Whether the drawing is flipped horizontally.
            flip_v: Whether the drawing is flipped vertically.
            interm_ln_pos: The position of the intermediate line.

        Returns:
            A tuple containing the directions of the head and tail.
        """
        # If the intermediate line is in the middle.
        if interm_ln_pos is None:
            head_direction = FourDirection.LEFT
            tail_direction = FourDirection.RIGHT
        elif abs(interm_ln_pos - 0) <= self.interm_ln_thrd:
            head_direction = FourDirection.UP
            tail_direction = FourDirection.RIGHT
        elif abs(interm_ln_pos - 100000) <= self.interm_ln_thrd:
            head_direction = FourDirection.LEFT
            tail_direction = FourDirection.DOWN
        elif interm_ln_pos > 100000:
            head_direction = FourDirection.LEFT
            tail_direction = FourDirection.LEFT
        elif interm_ln_pos < 0:
            head_direction = FourDirection.RIGHT
            tail_direction = FourDirection.RIGHT
        else:
            head_direction = FourDirection.LEFT
            tail_direction = FourDirection.RIGHT
        logger.info(
            f"origin id: {self.drawing.id}, head_direction: {head_direction}, tail_direction: {tail_direction}"
        )

        if rotation == 270 and flip_h:
            head_direction, tail_direction = tail_direction, head_direction
        # Rotate
        head_direction = head_direction.rotate(rotation // 90)
        tail_direction = tail_direction.rotate(rotation // 90)

        # Flip
        if flip_h:
            head_direction = head_direction.flip_h(rotation)
            tail_direction = tail_direction.flip_h(rotation)
        if flip_v:
            head_direction = head_direction.flip_v(rotation)
            tail_direction = tail_direction.flip_v(rotation)

        logger.info(
            f"rotate id: {self.drawing.id}, head_direction: {head_direction}, tail_direction: {tail_direction}"
        )

        logger.info(
            f"flip id: {self.drawing.id}, head_direction: {head_direction}, tail_direction: {tail_direction}"
        )
        return head_direction, tail_direction

    def convert(self) -> BentConnector3:
        """Converts the raw drawing to a BentConnector3 object.

        Returns:
            A BentConnector3 object.
        """
        x, y, w, h, rotation = self.convert_units()
        head_pos, tail_pos = self.calc_endpoints_pos(
            x, y, w, h, rotation, self.drawing.flip_h, self.drawing.flip_v
        )
        head_direction, tail_direction = self.extract_endpoints_direction(
            rotation,
            self.drawing.flip_h,
            self.drawing.flip_v,
            self.drawing.interm_line_pos,
        )
        arrow_type = self.extract_arrow_type()
        line_type = self.extract_line_style()
        line_color = self._convert_one_color(
            self.drawing.scheme_clr,
            self.drawing.srgb_clr,
            self.drawing.style_refs.ln_ref,
            self.theme,
        )
        line_width = self.drawing.arrow_line.width
        head_type = self.drawing.arrow_line.head.type
        tail_type = self.drawing.arrow_line.tail.type

        self.refined = BentConnector3(
            raw_id=self.drawing.id,
            name=self.drawing.name,
            drawing_id=self.id_counter,
            arrow_type=arrow_type,
            line_type=line_type,
            line_color=line_color,
            line_width=line_width,
            head_type=head_type,
            tail_type=tail_type,
            head_pos=head_pos,
            tail_pos=tail_pos,
            head_direction=head_direction,
            tail_direction=tail_direction,
        )
        return self.refined
