import math
from typing import Optional, TypeVar, Dict, Tuple
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

# Although it is actually 360000, 1000000 is adopted here for convenience
# EMU_TO_CM = 1 / 360000
EMU_TO_CM = 1 / 1000000

T = TypeVar("T")


def ensure_not_none(value: Optional[T], arg_name: str = "value") -> T:
    if value is None:
        raise ValueError(f"Invalid argument '{arg_name}': expected a non-None value")
    return value


def get_required_attribute(element: ET.Element, attr_name: str) -> str:
    """Retrieve a required attribute from an XML element.

    Args:
        element (ET.Element): The XML element to retrieve the attribute from.
        attr_name (str): The name of the attribute to retrieve.

    Returns:
        str: The value of the attribute.

    Raises:
        ValueError: If the attribute is missing.
    """
    value = ensure_not_none(element.get(attr_name), attr_name)
    return value


def get_required_element(
    element: ET.Element, path: str, namespaces: Optional[Dict[str, str]] = None
) -> ET.Element:
    """Retrieve a required child element from an XML element.

    Args:
        element (ET.Element): The XML element to retrieve the child from.
        path (str): The XPath to the child element.
        namespaces (Optional[Dict[str, str]]): XML namespaces to use during the search.

    Returns:
        ET.Element: The found child element.

    Raises:
        ValueError: If the child element is missing.
    """
    child = element.find(path, namespaces)
    if child is None:
        raise ValueError(f"Required element '{path}' is missing.")
    return child


def get_required_text(element: ET.Element) -> str:
    text = element.text
    if text is None:
        raise ValueError(f"Required element '{element}' is missing.")
    return text


def get_element_text(
    element: ET.Element, path: str, namespaces: Optional[Dict[str, str]] = None
) -> str:
    child = get_required_element(element, path, namespaces)
    text = get_required_text(child)
    return text


def get_attribute_or_none(
    element: ET.Element, attr_name: str, default: Optional[str] = None
) -> Optional[str]:
    return element.get(attr_name) or default


def get_attribute_or_default(element: ET.Element, attr_name: str, default: str) -> str:
    return element.get(attr_name) or default


def get_element_or_none(
    element: ET.Element, path: str, namespaces: Optional[Dict[str, str]] = None
) -> Optional[ET.Element]:
    child = element.find(path, namespaces)
    return child or None


def emu_to_cm(emu: float) -> float:
    """Convert EMU (English Metric Units) to centimeters.

    Args:
        emu (float): The value in EMU to be converted.

    Returns:
        float: The converted value in centimeters, rounded to two decimal places.
    """
    return round(emu * EMU_TO_CM, 2)


def apply_rotation(
    p: Tuple[float, float], c: Tuple[float, float], rotation: float
) -> Tuple[float, float]:
    """Apply rotation to a point around a center.

    Args:
        p (Tuple[float, float]): The point to be rotated.
        c (Tuple[float, float]): The center of rotation.
        rotation (float): The rotation angle in degrees.

    Returns:
        Tuple[float, float]: The new coordinates of the point after rotation.
    """
    # Calculate the center coordinates
    cx = c[0]
    cy = c[1]
    x = p[0]
    y = p[1]

    # Convert degrees to radians
    # Change to clockwise
    rad = math.radians(rotation)

    # Calculate new x, y
    new_x = cx + (x - cx) * math.cos(rad) - (y - cy) * math.sin(rad)
    new_y = cy + (x - cx) * math.sin(rad) + (y - cy) * math.cos(rad)
    return (new_x, new_y)


def apply_scale(x: float, y: float, w: float, h: float, scale: float) -> Tuple[float, float, float, float]:
    """Apply scaling to a rectangle defined by its top-left corner and dimensions.

    Args:
        x (float): The x-coordinate of the top-left corner.
        y (float): The y-coordinate of the top-left corner.
        w (float): The width of the rectangle.
        h (float): The height of the rectangle.
        scale (float): The scaling factor.

    Returns:
        Tuple[float, float, float, float]: The new coordinates and dimensions after scaling.
    """
    return x * scale, y * scale, w * scale, h * scale


def apply_flip(
    p: Tuple[float, float], c: Tuple[float, float], flip_h: bool, flip_v: bool
) -> Tuple[float, float]:
    """Apply horizontal and/or vertical flip to a point around a center.

    Args:
        p (Tuple[float, float]): The point to be flipped.
        c (Tuple[float, float]): The center of flipping.
        flip_h (bool): Whether to apply horizontal flip.
        flip_v (bool): Whether to apply vertical flip.

    Returns:
        Tuple[float, float]: The new coordinates of the point after flipping.
    """
    logger.info(f"flip_h: {flip_h}, flip_v: {flip_v}")
    if flip_h:
        logger.info(f"flip_h: {p}")
        p = (c[0] - (p[0] - c[0]), p[1])
    if flip_v:
        logger.info(f"flip_v: {p}")
        p = (p[0], c[1] - (p[1] - c[1]))
    return p
