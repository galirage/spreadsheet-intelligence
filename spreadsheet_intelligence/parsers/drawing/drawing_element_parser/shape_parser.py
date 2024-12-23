import xml.etree.ElementTree as ET
from .base_drawing_parser import (
    BaseDrawingParser,
)
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ShapeRaw,
    ShapeAnchorRaw,
)
from spreadsheet_intelligence.models.raw.drawing.anchor_models import Anchor
from spreadsheet_intelligence.utils.helpers import (
    get_required_attribute,
    get_required_element,
)


class ShapeParser(BaseDrawingParser[ShapeAnchorRaw, ShapeRaw]):
    """Parser for the shape element."""
    def _parse_text(self, text_el: ET.Element) -> str:
        """Parses the text element and returns the text string.

        Args:
            text_el (ET.Element): The text element.

        Returns:
            str: The parsed text string.

        Raises:
            ValueError: If the text element is not found.
        
        TODO:
        - Text parsing is not implemented when the text contains multiple formats.
        """
        text_element = text_el.find("xdr:txBody/a:p/a:r/a:t", self.namespaces)
        if text_element is not None and text_element.text is not None:
            return text_element.text.strip()
        else:
            raise ValueError("text_element is not found")

    def _parse_drawing(self, element: ET.Element) -> ShapeRaw:
        """Parses the drawing element and returns a ShapeRaw object.

        Args:
            element (ET.Element): The drawing element.

        Returns:
            ShapeRaw: The parsed ShapeRaw object.
        """
        sp_el = get_required_element(element, "xdr:sp", self.namespaces)
        id, name = self.parse_info(sp_el, "nvSpPr")

        prst_geom = get_required_element(sp_el, "xdr:spPr/a:prstGeom", self.namespaces)
        shape_type = get_required_attribute(prst_geom, "prst")

        ext_el = get_required_element(sp_el, "xdr:spPr/a:xfrm/a:ext", self.namespaces)
        off_el = get_required_element(sp_el, "xdr:spPr/a:xfrm/a:off", self.namespaces)
        width = int(get_required_attribute(ext_el, "cx"))
        height = int(get_required_attribute(ext_el, "cy"))
        x = int(get_required_attribute(off_el, "x"))
        y = int(get_required_attribute(off_el, "y"))

        try:
            ln_el = get_required_element(sp_el, "xdr:spPr/a:ln", self.namespaces)
            ln_scheme_clr, ln_srgb = self.parse_color(ln_el)
        except:
            ln_scheme_clr, ln_srgb = None, None

        # spPr is always present, so it's outside the try block.
        sp_pr = get_required_element(sp_el, "xdr:spPr", self.namespaces)
        try:
            fill_scheme_clr, fill_srgb = self.parse_color(sp_pr)
        except:
            fill_scheme_clr, fill_srgb = None, None

        # Parse <a:lnRef> and <a:fillRef> inside <a:style>
        try:
            style_el = get_required_element(sp_el, "xdr:style", self.namespaces)
            style_refs = self.parse_style_element(style_el)
        except ValueError as e:
            if "Required element 'xdr:style' is missing." in str(e):
                style_refs = None
            else:
                raise

        try:
            text_data = [self._parse_text(sp_el)]
        except ValueError:
            text_data = []

        return ShapeRaw(
            id=id,
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            shape_type=shape_type,
            fill_scheme_clr=fill_scheme_clr,
            fill_srgb_clr=fill_srgb,
            line_scheme_clr=ln_scheme_clr,
            line_srgb_clr=ln_srgb,
            style_refs=style_refs,
            text_data=text_data,
        )

    def _create_anchor_raw(
        self, anchor: Anchor, drawing_raw: ShapeRaw
    ) -> ShapeAnchorRaw:
        """Creates a ShapeAnchorRaw object.

        Args:
            anchor (Anchor): The anchor object.
            drawing_raw (ShapeRaw): The drawing raw object.

        Returns:
            ShapeAnchorRaw: The created ShapeAnchorRaw object.
        """
        return ShapeAnchorRaw(anchor, drawing_raw)
