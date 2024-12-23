import json
from typing import Any, Generic, Union
from spreadsheet_intelligence.models.converted.base_models import TBaseDrawingConverted
from spreadsheet_intelligence.models.converted.drawing_models import (
    BentConnector3,
    StraightConnector1,
    Shape,
)


class BaseFormatter(Generic[TBaseDrawingConverted]):
    """Base class for formatting drawing objects.

    Args:
        drawing (TBaseDrawingConverted): The drawing object to be formatted.
    """

    def __init__(self, drawing: TBaseDrawingConverted):
        self.drawing = drawing

    def format(self) -> dict:
        """Formats the drawing object.

        Returns:
            dict: The formatted dictionary representation of the drawing.
        """
        return {}


class BentConnectorFormatter(BaseFormatter[BentConnector3]):
    """Formatter for BentConnector3 objects."""

    def format(self) -> dict:
        """Formats a BentConnector3 object into a dictionary.

        Returns:
            dict: A dictionary representation of the BentConnector3 object.
        """
        format_dict: dict[str, str] = {}
        format_dict["id"] = str(self.drawing.drawing_id)
        format_dict["type"] = "bentConnector3"
        format_dict["arrowType"] = str(self.drawing.arrow_type)
        format_dict["color"] = "#" + self.drawing.line_color.hex_code
        format_dict["startX"] = f"{self.drawing.head_pos[0]:.2f}"
        format_dict["startY"] = f"{self.drawing.head_pos[1]:.2f}"
        format_dict["StartArrowHeadDirection"] = str(self.drawing.head_direction)
        format_dict["endX"] = f"{self.drawing.tail_pos[0]:.2f}"
        format_dict["endY"] = f"{self.drawing.tail_pos[1]:.2f}"
        format_dict["EndArrowHeadDirection"] = str(self.drawing.tail_direction)
        return format_dict


class StraightConnectorFormatter(BaseFormatter[StraightConnector1]):
    """Formatter for StraightConnector1 objects."""

    def format(self) -> dict:
        """Formats a StraightConnector1 object into a dictionary.

        Returns:
            dict: A dictionary representation of the StraightConnector1 object.
        """
        format_dict: dict[str, str] = {}
        format_dict["id"] = str(self.drawing.drawing_id)
        format_dict["type"] = "straightConnector1"
        format_dict["arrowType"] = str(self.drawing.arrow_type)
        format_dict["color"] = "#" + self.drawing.line_color.hex_code
        format_dict["startX"] = f"{self.drawing.head_pos[0]:.2f}"
        format_dict["startY"] = f"{self.drawing.head_pos[1]:.2f}"
        # StartArrowHeadDirection is not used for StraightConnector1
        format_dict["endX"] = f"{self.drawing.tail_pos[0]:.2f}"
        format_dict["endY"] = f"{self.drawing.tail_pos[1]:.2f}"
        # EndArrowHeadDirection is not used for StraightConnector1
        return format_dict


class ShapeFormatter(BaseFormatter[Shape]):
    """Formatter for Shape objects."""

    def format(self) -> dict:
        """Formats a Shape object into a dictionary.

        Returns:
            dict: A dictionary representation of the Shape object.
        """
        format_dict: dict[str, Union[str, dict]] = {}
        format_dict["id"] = str(self.drawing.drawing_id)
        format_dict["shapeType"] = str(self.drawing.shape_type)
        format_dict["fillColor"] = (
            ("#" + self.drawing.fill_color.hex_code)
            if self.drawing.fill_color
            else "None"
        )
        format_dict["borderColor"] = (
            ("#" + self.drawing.border_color.hex_code)
            if self.drawing.border_color
            else "None"
        )
        format_dict["left"] = f"{self.drawing.x:.2f}"
        format_dict["top"] = f"{self.drawing.y:.2f}"
        format_dict["right"] = f"{self.drawing.x + self.drawing.width:.2f}"
        format_dict["bottom"] = f"{self.drawing.y + self.drawing.height:.2f}"
        if self.drawing.text:
            format_dict["text"] = {}
            format_dict["text"]["content"] = self.drawing.text.content
            format_dict["text"]["fontColor"] = (
                "#" + self.drawing.text.font_color.hex_code
                if self.drawing.text.font_color
                else "None"
            )
            format_dict["text"]["fontSize"] = (
                self.drawing.text.font_size if self.drawing.text.font_size else "None"
            )
            format_dict["text"]["alignment"] = (
                self.drawing.text.alignment if self.drawing.text.alignment else "None"
            )
        else:
            format_dict["text"] = "None"
        return format_dict


class AllDrawingsFormatter:
    """Formatter for a list of drawing objects including connectors and shapes.

    Args:
        connector_list (list[Union[BentConnector3, StraightConnector1]]): List of connector objects.
        shape_list (list[Shape]): List of shape objects.
    """

    def __init__(
        self,
        connector_list: list[Union[BentConnector3, StraightConnector1]],
        shape_list: list[Shape],
    ):
        self.connector_list = connector_list
        self.shape_list = shape_list

    def format2json(self) -> str:
        """Formats all drawing objects into a JSON string.

        Returns:
            str: A JSON string representation of all drawing objects.
        """
        connector_json_list = []
        for connector in self.connector_list:
            if isinstance(connector, BentConnector3):
                connector_json_list.append(BentConnectorFormatter(connector).format())
            elif isinstance(connector, StraightConnector1):
                connector_json_list.append(
                    StraightConnectorFormatter(connector).format()
                )

        shape_json_list = [ShapeFormatter(shape).format() for shape in self.shape_list]
        return json.dumps(
            {"connectors": connector_json_list, "shapes": shape_json_list}, indent=4
        )
