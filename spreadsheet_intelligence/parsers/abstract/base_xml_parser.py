from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET


class BaseXMLParser(ABC):
    def __init__(self, xml_root: ET.Element):
        """Initializes the BaseXMLParser with the root of the XML document.

        Args:
            xml_root (ET.Element): The root element of the XML document.
        """
        self.xml_root = xml_root
        self.namespaces: dict[str, str] = {}  # Override with the namespace for each XML

    @abstractmethod
    def parse(self):
        """Abstract method to parse the XML document.

        This method should be implemented by subclasses to define
        specific parsing logic.
        """
        pass
