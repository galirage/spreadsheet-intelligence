import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree, ParseError


class XMLLoaderError(Exception):
    pass


class XMLLoader:
    def __init__(self, xml_path: str):
        """
        Args:
            xml_path (str): Path to the XML file
        """
        self.xml_path = xml_path

    def load_tree(self) -> ElementTree:
        """
        Load the specified XML file as an ElementTree.

        Returns:
            ElementTree: Parsed ElementTree object.

        Raises:
            XMLLoaderError: If the file does not exist, access is denied, or a parse error occurs.
        """
        try:
            tree = ET.parse(self.xml_path)
            return tree
        except (FileNotFoundError, PermissionError, ParseError) as e:
            raise XMLLoaderError(
                f"Failed to load XML from {self.xml_path}: {str(e)}"
            ) from e

    def get_root(self) -> Element:
        """
        Get the root element of the XML.

        Returns:
            Element: Root element
        """
        tree = self.load_tree()
        return tree.getroot()
