import logging
from typing import List, Tuple
import xml.etree.ElementTree as ET
from spreadsheet_intelligence.parsers.abstract.base_xml_parser import BaseXMLParser
from spreadsheet_intelligence.utils.helpers import get_required_element
from .drawing_element_parser.connector_parser import ConnectorParser
from .drawing_element_parser.shape_parser import ShapeParser
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ConnectorAnchorRaw,
)
from spreadsheet_intelligence.models.raw.drawing.drawing_models import ShapeAnchorRaw

logger = logging.getLogger(__name__)


class DrawingXMLParser(BaseXMLParser):
    """Parses XML elements related to drawing objects in a spreadsheet.

    This class is responsible for parsing XML elements that represent
    drawing objects such as connectors and shapes in a spreadsheet.

    Attributes:
        namespaces (dict): XML namespaces used in the drawing XML.
        xml_root (ET.Element): Root element of the drawing XML.
        connector_list (List[ConnectorAnchorRaw]): List of parsed connector anchors.
        shape_list (List[ShapeAnchorRaw]): List of parsed shape anchors.
    """

    def __init__(self, drawing_root: ET.Element):
        """Initializes the DrawingXMLParser with the root XML element.

        Args:
            drawing_root (ET.Element): The root element of the drawing XML.
        """
        self.namespaces = {
            "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        }
        self.xml_root = drawing_root
        logger.debug(f"DrawingXMLParser | __init__ | drawing_root: {drawing_root.tag}")
        self.connector_list: List[ConnectorAnchorRaw] = []
        self.shape_list: List[ShapeAnchorRaw] = []

    def parse(self) -> Tuple[List[ConnectorAnchorRaw], List[ShapeAnchorRaw]]:
        """Parses the drawing XML to extract connectors and shapes.

        Iterates over the XML elements to find and parse connectors and shapes,
        storing them in their respective lists.

        Returns:
            Tuple[List[ConnectorAnchorRaw], List[ShapeAnchorRaw]]: A tuple containing
            lists of parsed connector and shape anchors.
        """
        for twocell_anchor_el in self.xml_root.findall(
            "xdr:twoCellAnchor", self.namespaces
        ):
            logger.debug(f"DrawingXMLParser | parse | parsing {twocell_anchor_el}")
            # Check if the element is a connector
            if twocell_anchor_el.find("xdr:cxnSp", self.namespaces) is not None:
                logger.info("Parsing connector")
                connector_parser = ConnectorParser(self.namespaces)
                connector_anchor_raw = connector_parser.parse(twocell_anchor_el)
                self.connector_list.append(connector_anchor_raw)
            # Check if the element is a shape
            elif twocell_anchor_el.find("xdr:sp", self.namespaces) is not None:
                logger.info("Parsing shape")
                shape_parser = ShapeParser(self.namespaces)
                shape_anchor_raw = shape_parser.parse(twocell_anchor_el)
                self.shape_list.append(shape_anchor_raw)
        return self.connector_list, self.shape_list
