from abc import ABC, abstractmethod
from typing import Dict
import xml.etree.ElementTree as ET


class BaseParser(ABC):
    def __init__(self, namespaces: Dict[str, str]):
        self.namespaces = namespaces

    @abstractmethod
    def parse(self, element: ET.Element):
        pass
