import logging
from typing import Optional
import xml.etree.ElementTree as ET
from spreadsheet_intelligence.parsers.abstract.base_xml_parser import BaseXMLParser
from .theme_element_parser.theme_parser import ThemeParser
from spreadsheet_intelligence.models.raw.theme.theme_models import Theme
from spreadsheet_intelligence.utils.helpers import get_required_element

logger = logging.getLogger(__name__)


class ThemeXMLParser(BaseXMLParser):
    """Parses XML theme elements into a Theme object.

    Attributes:
        namespaces (dict): XML namespaces used in the theme.
        theme_el_root (ET.Element): Root element of the theme XML.
        theme (Optional[Theme]): Parsed theme object.
    """

    def __init__(self, theme_root: ET.Element):
        """Initializes ThemeXMLParser with the root XML element.

        Args:
            theme_root (ET.Element): The root element of the theme XML.
        """
        self.namespaces = {
            "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        }
        self.theme_el_root = get_required_element(
            theme_root, "a:themeElements", self.namespaces
        )
        self.theme: Optional[Theme] = None

    def parse(self) -> Theme:
        """Parses the theme XML and returns a Theme object.

        Returns:
            Theme: The parsed theme object.
        """
        theme_parser = ThemeParser(self.namespaces)
        self.theme = theme_parser.parse(self.theme_el_root)
        return self.theme
