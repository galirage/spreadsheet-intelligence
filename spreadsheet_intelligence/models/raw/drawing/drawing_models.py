from dataclasses import dataclass
from typing import Optional, List
from spreadsheet_intelligence.models.raw.drawing.base_models import (
    BaseDrawingRaw,
    BaseAnchorRaw,
)
from spreadsheet_intelligence.models.common.enums import ConnectorType
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    SchemeClr,
    SrgbClr,
    StyleRefs,
)


@dataclass
class ArrowHead:
    """
    Represents an arrow head of a connector with type, width, and length.

    XMLReference:
        type: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln/xdr:headEnd(tailEnd) >> type
        width: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln/xdr:headEnd(tailEnd) >> w
        length: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln/xdr:headEnd(tailEnd) >> len
    """
    type: str
    width: Optional[str]
    length: Optional[str]


@dataclass
class ArrowLine:
    """
    Represents an arrow line of a connector with width, cap, compound, alignment, dash style, and arrow heads.

    XMLReference:
        width: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln >> w
        cap: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln >> cap
        compound: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln >> cmpd
        alignment: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln >> algn
        dash_style: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln/xdr:prstDash >> val
        head: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln/xdr:headEnd
        tail: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln/xdr:tailEnd
    """
    width: int
    cap: Optional[str] # this is not parsed in the current parser
    compound: Optional[str] # this is not parsed in the current parser
    alignment: Optional[str] # this is not parsed in the current parser
    dash_style: str
    head: ArrowHead
    tail: ArrowHead


@dataclass
class ConnectorRaw(BaseDrawingRaw):
    """
    Represents information shared by all connector types, including type, flip, rotation, line data, intermediate line position, style references, and color data.

    Attributes:
        connector_type (ConnectorType): The type of connector.
        flip_h (bool): Whether the connector is flipped horizontally.
        flip_v (bool): Whether the connector is flipped vertically.
        rotation (float): The rotation of the connector in degrees.
        arrow_line (ArrowLine): The line data for the connector.
        interm_line_pos (Optional[int]): The position of the intermediate line.
        style_refs (StyleRefs): The style references for the connector.
        scheme_clr (Optional[SchemeClr]): The scheme color for the connector.
        srgb_clr (Optional[SrgbClr]): The sRGB color for the connector.

    XMLReference:
        connector_type: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:prstGeom >> prst
        flip_h: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:xfrm >> flipH
        flip_v: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:xfrm >> flipV
        rotation: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:xfrm >> rot
        arrow_line: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:ln
        interm_line_pos: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:spPr/xdr:prstGeom/xdr:avLst/xdr:gd >> fmla
        style_refs: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:style/a:lnRef >> idx
        scheme_clr: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:style/a:lnRef/a:schemeClr >> val
        srgb_clr: xl/drawingX.xml/xdr:twoCellAnchor/xdr:cxnSp/xdr:style/a:lnRef/a:srgbClr >> val
    """
    connector_type: ConnectorType
    flip_h: bool
    flip_v: bool
    rotation: float
    arrow_line: ArrowLine
    interm_line_pos: Optional[int]
    style_refs: StyleRefs
    scheme_clr: Optional[SchemeClr]
    srgb_clr: Optional[SrgbClr]


@dataclass
class PictureRaw(BaseDrawingRaw):
    image_path: str


@dataclass
class ShapeRaw(BaseDrawingRaw):
    """
    Represents a shape with type, fill color, line color, style references, and text data.

    Attributes:
        shape_type (str): The type of shape.
        fill_scheme_clr (Optional[SchemeClr]): The scheme color for the fill.
        fill_srgb_clr (Optional[SrgbClr]): The sRGB color for the fill.
        line_scheme_clr (Optional[SchemeClr]): The scheme color for the line.
        line_srgb_clr (Optional[SrgbClr]): The sRGB color for the line.
        style_refs (Optional[StyleRefs]): The style references for the shape.
        text_data (List[str]): The text data for the shape.
    
    XMLReference:
        shape_type: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:prstGeom >> prst
        fill_scheme_clr: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:solidFill/a:schemeClr >> val
        fill_srgb_clr: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:solidFill/a:srgbClr >> val
        line_scheme_clr: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:ln/a:solidFill/a:schemeClr >> val
        line_srgb_clr: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:ln/a:solidFill/a:srgbClr >> val
        style_refs: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:style
        text_data: xl/drawingX.xml/xdr:twoCellAnchor/xdr:spPr/a:txBody/a:bodyPr/a:textAlignment >> val
    
    TODO:
        - Text data with multiple formats is not yet parsed
    """
    shape_type: str
    fill_scheme_clr: Optional[SchemeClr]
    fill_srgb_clr: Optional[SrgbClr]
    line_scheme_clr: Optional[SchemeClr]
    line_srgb_clr: Optional[SrgbClr]
    style_refs: Optional[StyleRefs]
    text_data: List[str]


@dataclass
class ConnectorAnchorRaw(BaseAnchorRaw[ConnectorRaw]):
    """
    Represents an anchor point for a connector with a connector data.

    Attributes:
        anchor (Anchor): The anchor point for the connector.
        drawing (ConnectorRaw): The connector data associated with the anchor.
    """
    pass


@dataclass
class PictureAnchorRaw(BaseAnchorRaw[PictureRaw]):
    """
    Represents an anchor point for a picture with a picture data.

    Attributes:
        anchor (Anchor): The anchor point for the picture.
        drawing (PictureRaw): The picture data associated with the anchor.
    """
    pass


@dataclass
class ShapeAnchorRaw(BaseAnchorRaw[ShapeRaw]):
    """
    Represents an anchor point for a shape with a shape data.

    Attributes:
        anchor (Anchor): The anchor point for the shape.
        drawing (ShapeRaw): The shape data associated with the anchor.
    """
    pass
