from warnings import warn
import xml.etree.ElementTree as ET
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ConnectorRaw,
    ConnectorAnchorRaw,
    ArrowLine,
    ArrowHead,
)
from spreadsheet_intelligence.models.raw.drawing.anchor_models import Anchor
from .base_drawing_parser import (
    BaseDrawingParser,
)
from spreadsheet_intelligence.utils.helpers import (
    get_required_attribute,
    get_required_element,
    get_attribute_or_none,
    get_attribute_or_default,
)
from spreadsheet_intelligence.models.common.enums import ConnectorType


class ConnectorParser(BaseDrawingParser[ConnectorAnchorRaw, ConnectorRaw]):
    """Parser for the connector element."""
    def parse_line_element(self, line_el: ET.Element) -> ArrowLine:
        """Parses the <a:ln> element and returns an ArrowLine type.

        Args:
            line_el (ET.Element): The <a:ln> element.

        Returns:
            ArrowLine: The ArrowLine type.
        """
        # Retrieve basic attributes
        # There are other attributes in a:ln, but they are not used in this parser.
        width = int(
            line_el.get("w", "25400")
        )  # Default value is 25400 (corresponds to the initial value of 2 pt in Excel)

        # Retrieve dash style
        dash_el = line_el.find("a:prstDash", self.namespaces)
        if dash_el is not None:
            dash_style = get_required_attribute(dash_el, "val")
        else:
            dash_style = "none"

        # Retrieve arrow settings (stealth, triangle, none)
        head_end = line_el.find("a:headEnd", self.namespaces)
        if head_end is not None:
            head_end_type = get_required_attribute(head_end, "type")
        else:
            head_end_type = "none"
        tail_end = line_el.find("a:tailEnd", self.namespaces)
        if tail_end is not None:
            tail_end_type = get_required_attribute(tail_end, "type")
        else:
            tail_end_type = "none"

        return ArrowLine(
            width=width,
            dash_style=dash_style,
            cap=None, # this is not parsed in the current parser
            compound=None, # this is not parsed in the current parser
            alignment=None, # this is not parsed in the current parser
            head=ArrowHead(type=head_end_type, width=None, length=None),
            tail=ArrowHead(type=tail_end_type, width=None, length=None),
        )

    def parse_text(self, text_el: ET.Element) -> str:
        """Parses the <xdr:txBody> element and returns a text string.

        Args:
            text_el (ET.Element): The <xdr:txBody> element.

        Returns:
            str: The text string.

        Raises:
            ValueError: If the text element is not found.
        
        TODO:
        - Text parsing is not implemented when the text contains multiple formats.
        """
        text_element = text_el.find("xdr:txBody/a:p/a:r/a:t", self.namespaces)
        if text_element is not None and text_element.text is not None:
            return text_element.text.strip()
        else:
            raise ValueError("Text element is not found")

    def _parse_drawing(self, element: ET.Element) -> ConnectorRaw:
        """Parses the drawing element and returns a ConnectorRaw object.

        Args:
            element (ET.Element): The drawing element.

        Returns:
            ConnectorRaw: The parsed ConnectorRaw object.
        """
        cxnsp_el = get_required_element(element, "xdr:cxnSp", self.namespaces)
        id, name = self.parse_info(cxnsp_el, "nvCxnSpPr")

        prst_geom = get_required_element(
            cxnsp_el, "xdr:spPr/a:prstGeom", self.namespaces
        )
        connector_type_str = get_required_attribute(prst_geom, "prst")

        interm_line_pos = None
        if connector_type_str == "bentConnector3":
            connector_type = ConnectorType.BENT_CONNECTOR_3
            interm_line_el = prst_geom.find("a:avLst/a:gd", self.namespaces)
            if interm_line_el is not None:
                interm_line_pos_str = get_required_attribute(interm_line_el, "fmla")
                interm_line_pos_splt = interm_line_pos_str.split(" ")
                if len(interm_line_pos_splt) == 2:
                    interm_line_pos = int(interm_line_pos_splt[1])
                else:
                    raise ValueError(
                        "Intermediate line position is not valid. Expected format: 'x y'"
                    )
        elif connector_type_str == "straightConnector1":
            connector_type = ConnectorType.STRAIGHT_CONNECTOR_1
        else:
            warn(f"Unsupported connector type: {connector_type_str}")

        # Parsing the xfrm element
        xfrm_el = get_required_element(cxnsp_el, "xdr:spPr/a:xfrm", self.namespaces)
        ext_el = get_required_element(xfrm_el, "a:ext", self.namespaces)
        off_el = get_required_element(xfrm_el, "a:off", self.namespaces)
        width = int(get_required_attribute(ext_el, "cx"))
        height = int(get_required_attribute(ext_el, "cy"))
        x = int(get_required_attribute(off_el, "x"))
        y = int(get_required_attribute(off_el, "y"))
        flip_h = get_attribute_or_none(xfrm_el, "flipH") == "1"
        flip_v = get_attribute_or_none(xfrm_el, "flipV") == "1"
        rotation = int(get_attribute_or_default(xfrm_el, "rot", default="0"))

        # Parsing line
        line_el = get_required_element(cxnsp_el, "xdr:spPr/a:ln", self.namespaces)
        arrow_line = self.parse_line_element(line_el)

        # Style, color
        scheme_clr, srgb = self.parse_color(line_el)

        style_refs = self.parse_style_element(
            get_required_element(cxnsp_el, "xdr:style", self.namespaces)
        )

        return ConnectorRaw(
            id=id,
            name=name,
            connector_type=connector_type,
            x=x,
            y=y,
            width=width,
            height=height,
            flip_h=flip_h,
            flip_v=flip_v,
            rotation=rotation,
            arrow_line=arrow_line,
            interm_line_pos=interm_line_pos,
            style_refs=style_refs,
            scheme_clr=scheme_clr,
            srgb_clr=srgb,
        )

    def _create_anchor_raw(
        self, anchor: Anchor, drawing_raw: ConnectorRaw
    ) -> ConnectorAnchorRaw:
        """Creates a ConnectorAnchorRaw object.

        Args:
            anchor (Anchor): The anchor object.
            drawing_raw (ConnectorRaw): The drawing raw object.

        Returns:
            ConnectorAnchorRaw: The created ConnectorAnchorRaw object.
        """
        return ConnectorAnchorRaw(anchor, drawing_raw)
