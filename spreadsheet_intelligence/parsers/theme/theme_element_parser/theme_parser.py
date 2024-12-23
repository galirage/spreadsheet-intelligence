from abc import ABC, abstractmethod
from typing import Dict, Union
import xml.etree.ElementTree as ET
from spreadsheet_intelligence.parsers.abstract.base_parser import BaseParser
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    Theme,
    ClrScheme,
    SrgbClr,
    SysClr,
    Color,
)
from spreadsheet_intelligence.utils.helpers import get_required_element


class ThemeParser(BaseParser):
    """Parser for theme elements in a spreadsheet.

    This class is responsible for parsing XML elements related to themes
    and converting them into Theme objects.

    Attributes:
        namespaces (dict[str, str]): A dictionary of XML namespaces.
    """

    def __init__(self, namespaces: dict[str, str]):
        """Initializes the ThemeParser with the given namespaces.

        Args:
            namespaces (dict[str, str]): A dictionary of XML namespaces.
        """
        super().__init__(namespaces)

    def parse(self, element: ET.Element) -> Theme:
        """Parses a theme element and returns a Theme object.

        Args:
            element (ET.Element): The XML element to parse.

        Returns:
            Theme: The parsed Theme object.
        """
        clr_scheme_el = get_required_element(element, "a:clrScheme", self.namespaces)
        clr_scheme = self._parse_clr_scheme(clr_scheme_el)
        return Theme(clr_scheme)

    def _parse_clr_scheme(self, element: ET.Element) -> ClrScheme:
        """Parses a color scheme element and returns a ClrScheme object.

        Args:
            element (ET.Element): The XML element representing the color scheme.

        Returns:
            ClrScheme: The parsed ClrScheme object.
        """
        clr_scheme_data: dict[str, Union[SrgbClr, SysClr]] = {}
        for child in element:
            tag = child.tag.split("}")[1]  # Remove namespace
            for subchild in child:
                subtag = subchild.tag.split("}")[1]
                if "val" in subchild.attrib:
                    val = subchild.attrib["val"]
                if "lastClr" in subchild.attrib:
                    last_clr = subchild.attrib["lastClr"]

                if subtag == "srgbClr":
                    clr_scheme_data[tag] = SrgbClr(Color(val))
                elif subtag == "sysClr":
                    clr_scheme_data[tag] = SysClr(val, Color(last_clr))
        return ClrScheme(**clr_scheme_data)
