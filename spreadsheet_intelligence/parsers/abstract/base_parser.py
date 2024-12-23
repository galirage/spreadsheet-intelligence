import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseParser(ABC):
    """Abstract base class for XML parsers.

    This class provides a template for creating XML parsers with specific namespaces.

    Attributes:
        namespaces (Dict[str, str]): A dictionary mapping namespace prefixes to URIs.
    """

    def __init__(self, namespaces: Dict[str, str]):
        """Initializes the BaseParser with the given namespaces.

        Args:
            namespaces (Dict[str, str]): A dictionary of namespace prefixes and URIs.
        """
        self.namespaces = namespaces

    @abstractmethod
    def parse(self, element: ET.Element) -> Any:
        """Parses an XML element.

        This method should be implemented by subclasses to define specific parsing logic.

        Args:
            element (ET.Element): The XML element to parse.

        Returns:
            Any: The result of parsing the XML element.
        """
        pass
