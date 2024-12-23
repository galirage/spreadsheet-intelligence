from dataclasses import dataclass


@dataclass
class AnchorPoint:
    """
    Represents an anchor point with column and row coordinates.

    Args:
        col (int): The column index of the anchor point.
        colOff (int): The column offset of the anchor point.
        row (int): The row index of the anchor point.
        rowOff (int): The row offset of the anchor point.
    
    XMLReference:
        col: drawingX.xml/xdr:twoCellAnchor/xdr:from/xdr:col
        colOff: drawingX.xml/xdr:twoCellAnchor/xdr:from/xdr:colOff
        row: drawingX.xml/xdr:twoCellAnchor/xdr:from/xdr:row
        rowOff: drawingX.xml/xdr:twoCellAnchor/xdr:from/xdr:rowOff
    """
    col: int
    colOff: int
    row: int
    rowOff: int


@dataclass
class Anchor:
    """
    Represents an anchor with two points.

    Args:
        from_point (AnchorPoint): The starting point of the anchor.
        to_point (AnchorPoint): The ending point of the anchor.

    XMLReference:
        from_point: drawingX.xml/xdr:twoCellAnchor/xdr:from
        to_point: drawingX.xml/xdr:twoCellAnchor/xdr:to
    """
    from_point: AnchorPoint
    to_point: AnchorPoint

