from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic
from spreadsheet_intelligence.models.raw.drawing.anchor_models import Anchor


@dataclass
class BaseDrawingRaw(ABC):
    """
    Base class for raw drawing objects.

    Args:
        id (str): Unique identifier for the drawing.
        name (str): Name of the drawing.
        x (int): X-coordinate of the drawing's position.
        y (int): Y-coordinate of the drawing's position.
        width (int): Width of the drawing.
        height (int): Height of the drawing.
    
    XMLReference:
        id: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(CxnSp)/xdr:nvSpPr(nvCxnSpPr)/xdr:cNvPr >> id
        name: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(CxnSp)/xdr:nvSpPr(nvCxnSpPr)/xdr:cNvPr >> name
        x: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(CxnSp)/xdr:spPr/xdr:xfrm/xdr:off >> x
        y: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(CxnSp)/xdr:spPr/xdr:xfrm/xdr:off >> y
        width: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(CxnSp)/xdr:spPr/xdr:xfrm/xdr:ext >> cx
        height: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(CxnSp)/xdr:spPr/xdr:xfrm/xdr:ext >> cy
    """
    id: str
    name: str
    x: int
    y: int
    width: int
    height: int


TBaseDrawingRaw = TypeVar("TBaseDrawingRaw", bound=BaseDrawingRaw)


@dataclass
class BaseAnchorRaw(ABC, Generic[TBaseDrawingRaw]):
    """
    Base class for raw anchor objects that associate with a drawing.

    Attributes:
        anchor (Anchor): The anchor point for the drawing.
        drawing (TBaseDrawingRaw): The drawing associated with the anchor.
    
    XMLReference:
        anchor: xl/drawingX.xml/xdr:twoCellAnchor/xdr:from, xdr:to
        drawing: xl/drawingX.xml/xdr:twoCellAnchor/xdr:sp(cxnSp)
    """
    anchor: Anchor
    drawing: TBaseDrawingRaw


TBaseAnchorRaw = TypeVar("TBaseAnchorRaw", bound=BaseAnchorRaw)
