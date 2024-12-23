from abc import ABC
from dataclasses import dataclass
from typing import TypeVar


@dataclass
class BaseDrawingConverted(ABC):
    """
    Base class for converted drawing objects.

    Attributes:
        raw_id (str): The raw identifier of the drawing.
        name (str): The name of the drawing.
        drawing_id (int): The unique identifier for the drawing.
    """
    raw_id: str
    name: str
    drawing_id: int


TBaseDrawingConverted = TypeVar("TBaseDrawingConverted", bound=BaseDrawingConverted)
