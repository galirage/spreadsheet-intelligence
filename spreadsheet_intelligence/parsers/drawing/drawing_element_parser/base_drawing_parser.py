# base_parser.py
from abc import ABC, abstractmethod
from typing import Dict, Generic
import xml.etree.ElementTree as ET

from spreadsheet_intelligence.models.raw.drawing.base_models import (
    TBaseAnchorRaw,
    TBaseDrawingRaw,
)
from spreadsheet_intelligence.models.raw.drawing.anchor_models import (
    Anchor,
    AnchorPoint,
)
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    StyleBaseRef,
    StyleRefs,
    SchemeClr,
    SrgbClr,
    Color,
)
from spreadsheet_intelligence.parsers.common.common_parser import (
    get_scheme_clr,
    get_srgb_clr,
)
from spreadsheet_intelligence.utils.helpers import (
    get_required_element,
    get_element_text,
    get_required_attribute,
)
from spreadsheet_intelligence.parsers.abstract.base_parser import BaseParser


def parse_anchor_point(element: ET.Element, namespaces: Dict[str, str]) -> AnchorPoint:
    """Parses an anchor point from the given XML element.

    Args:
        element (ET.Element): The XML element containing the anchor point.
        namespaces (Dict[str, str]): The XML namespaces.

    Returns:
        AnchorPoint: The parsed anchor point.
    """
    col = int(get_element_text(element, "xdr:col", namespaces))
    colOff = int(get_element_text(element, "xdr:colOff", namespaces))
    row = int(get_element_text(element, "xdr:row", namespaces))
    rowOff = int(get_element_text(element, "xdr:rowOff", namespaces))
    return AnchorPoint(col, colOff, row, rowOff)


def parse_anchor(element: ET.Element, namespaces: Dict[str, str]) -> Anchor:
    """Parses an anchor from the given XML element.

    Args:
        element (ET.Element): The XML element containing the anchor.
        namespaces (Dict[str, str]): The XML namespaces.

    Returns:
        Anchor: The parsed anchor.
    """
    from_point = parse_anchor_point(
        get_required_element(element, "xdr:from", namespaces), namespaces
    )
    to_point = parse_anchor_point(
        get_required_element(element, "xdr:to", namespaces), namespaces
    )
    return Anchor(from_point, to_point)


class BaseDrawingParser(BaseParser, ABC, Generic[TBaseAnchorRaw, TBaseDrawingRaw]):
    def __init__(self, namespaces: dict[str, str]):
        """Initializes the BaseDrawingParser with the given namespaces.

        Args:
            namespaces (dict[str, str]): The XML namespaces.
        """
        super().__init__(namespaces)

    def parse_anchor(self, twocellanchor_element: ET.Element) -> Anchor:
        """Parses an anchor and returns the model.

        Args:
            twocellanchor_element (ET.Element): The XML element containing the two-cell anchor.

        Returns:
            Anchor: The parsed anchor.
        """
        anchor = parse_anchor(twocellanchor_element, self.namespaces)
        return anchor

    def parse_info(self, sp_el: ET.Element, nv_tag_name: str) -> tuple[str, str]:
        """Parses drawing id and name.

        Args:
            sp_el (ET.Element): The XML element containing the drawing information.
            nv_tag_name (str): The tag name for the non-visual properties.

        Returns:
            tuple[str, str]: A tuple containing the id and name.
        """
        cnv_pr_el = get_required_element(
            sp_el, f"xdr:{nv_tag_name}/xdr:cNvPr", self.namespaces
        )
        id = get_required_attribute(cnv_pr_el, "id")
        name = get_required_attribute(cnv_pr_el, "name")
        return id, name

    def parse_style_ref_el(self, style_ref_el: ET.Element) -> StyleBaseRef:
        """Parses elements like <a:lnRef> and <a:fillRef> under <xdr:style> and returns a StyleBaseRef type.

        Args:
            style_ref_el (ET.Element): Elements like <a:lnRef> and <a:fillRef> under <xdr:style>.

        Raises:
            ValueError: If neither schemeClr nor scrgbClr is present.

        Returns:
            StyleBaseRef: Returns schemeClr if both schemeClr and scrgbClr are present. Returns scrgbClr if only scrgbClr is present.
        """
        scheme_clr_el = style_ref_el.find("a:schemeClr", namespaces=self.namespaces)
        scrgb_clr_el = style_ref_el.find("a:scrgbClr", namespaces=self.namespaces)
        idx = get_required_attribute(style_ref_el, "idx")
        if scheme_clr_el is not None:
            return StyleBaseRef(
                idx=idx, ref_clr=get_scheme_clr(scheme_clr_el, self.namespaces)
            )
        elif scrgb_clr_el is not None:
            r = int(get_required_attribute(scrgb_clr_el, "r"))
            g = int(get_required_attribute(scrgb_clr_el, "g"))
            b = int(get_required_attribute(scrgb_clr_el, "b"))
            return StyleBaseRef(idx=idx, ref_clr=SrgbClr(Color(r=r, g=g, b=b)))
        else:
            raise ValueError("Neither schemeClr nor scrgbClr is found")

    def parse_style_element(self, style_el: ET.Element) -> StyleRefs:
        """Parses the <xdr:style> element and returns a StyleRefs type.

        Args:
            style_el (ET.Element): The <xdr:style> element.

        Returns:
            StyleRefs: A class that consolidates the four elements: lnRef, fillRef, effectRef, and fontRef.
        """
        ln_ref = self.parse_style_ref_el(
            get_required_element(style_el, "a:lnRef", self.namespaces)
        )
        fill_ref = self.parse_style_ref_el(
            get_required_element(style_el, "a:fillRef", self.namespaces)
        )
        # TODO: if effectRef and fontRef are needed, add them
        return StyleRefs(
            ln_ref=ln_ref,
            fill_ref=fill_ref,
            effect_ref=None,
            font_ref=None,
        )

    def parse_color(
        self, parent_el: ET.Element
    ) -> tuple[SchemeClr | None, SrgbClr | None]:
        """Parses color from xdr:spPr/a:ln or xdr:spPr(solidFill).

        Args:
            parent_el (ET.Element): When borderColor, parent_el is xdr:spPr/a:ln; when fillColor, parent_el is xdr:spPr.

        Returns:
            tuple[SchemeClr | None, SrgbClr | None]: A tuple containing SchemeClr and SrgbClr.
        """
        try:
            scheme_parent_el = get_required_element(
                parent_el, "a:solidFill/a:schemeClr", self.namespaces
            )
            scheme_clr = get_scheme_clr(scheme_parent_el, self.namespaces)
        except:
            scheme_clr = None
        try:
            srgb_parent_el = get_required_element(
                parent_el, "a:solidFill/a:srgbClr", self.namespaces
            )
            srgb = get_srgb_clr(srgb_parent_el)
        except:
            srgb = None
        return scheme_clr, srgb

    @abstractmethod
    def _parse_drawing(self, twocellanchor_element: ET.Element) -> TBaseDrawingRaw:
        """Abstract method to parse a drawing element.

        Args:
            twocellanchor_element (ET.Element): The XML element containing the two-cell anchor.

        Returns:
            TBaseDrawingRaw: The parsed drawing raw data.
        """
        pass

    @abstractmethod
    def _create_anchor_raw(
        self, anchor: Anchor, drawing_raw: TBaseDrawingRaw
    ) -> TBaseAnchorRaw:
        """Abstract method to create an anchor raw model.

        Args:
            anchor (Anchor): The parsed anchor.
            drawing_raw (TBaseDrawingRaw): The parsed drawing raw data.

        Returns:
            TBaseAnchorRaw: The created anchor raw model.
        """
        pass

    def parse(self, twocellanchor_element: ET.Element) -> TBaseAnchorRaw:
        """Parses an element and returns the model.

        Args:
            twocellanchor_element (ET.Element): The XML element containing the two-cell anchor.

        Returns:
            TBaseAnchorRaw: The parsed anchor raw model.
        """
        anchor = self.parse_anchor(twocellanchor_element)
        drawing_raw = self._parse_drawing(twocellanchor_element)
        return self._create_anchor_raw(anchor, drawing_raw)
