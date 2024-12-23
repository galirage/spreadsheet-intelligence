from typing import Dict
import xml.etree.ElementTree as ET
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    SchemeClr,
    SrgbClr,
    Color,
)
from spreadsheet_intelligence.utils.helpers import get_required_attribute


def get_scheme_clr(scheme_clr_el: ET.Element, namespaces: Dict[str, str]) -> SchemeClr:
    """Extracts SchemeClr from an XML element.

    Args:
        scheme_clr_el (ET.Element): The XML element containing the scheme color.
        namespaces (Dict[str, str]): A dictionary of XML namespaces.

    Returns:
        SchemeClr: The extracted scheme color object.

    Raises:
        ValueError: If the 'val' attribute is not found in the element.
    """
    try:
        val = get_required_attribute(scheme_clr_el, "val")
    except:
        raise ValueError(f"Value not found in {scheme_clr_el.tag}.")

    # Find and convert 'lumMod' attribute if it exists
    lum_mod_el = scheme_clr_el.find("a:lumMod", namespaces)
    if lum_mod_el is not None:
        lum_mod = int(get_required_attribute(lum_mod_el, "val"))
    else:
        lum_mod = None

    # Find and convert 'lumOff' attribute if it exists
    lum_off_el = scheme_clr_el.find("a:lumOff", namespaces)
    if lum_off_el is not None:
        lum_off = int(get_required_attribute(lum_off_el, "val"))
    else:
        lum_off = None

    # Find and convert 'shade' attribute if it exists
    shade_el = scheme_clr_el.find("a:shade", namespaces)
    if shade_el is not None:
        shade = int(get_required_attribute(shade_el, "val"))
    else:
        shade = None

    return SchemeClr(val, lum_mod, lum_off, shade)


def get_srgb_clr(srgb_clr_el: ET.Element) -> SrgbClr:
    """Extracts SrgbClr from an XML element.

    Args:
        srgb_clr_el (ET.Element): The XML element containing the sRGB color.

    Returns:
        SrgbClr: The extracted sRGB color object.

    Raises:
        ValueError: If the 'val' attribute is not found in the element.
    """
    try:
        val = get_required_attribute(srgb_clr_el, "val")
    except:
        raise ValueError(f"Value not found in {srgb_clr_el.tag}.")
    return SrgbClr(Color(val))
