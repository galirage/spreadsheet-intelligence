# Spreadsheet Intelligence

A package for intelligent spreadsheet processing.




- parser, converter, loader, utils


# List of parsed elements
- x/drawingX.xml
  - xdr:twoCellAnchor | the bounding box data of the drawing
    - xdr:from
      - xdr:col
      - xdr:colOff
      - xdr:row
      - xdr:rowOff
    - xdr:to
      - xdr:col
      - xdr:colOff
      - xdr:row
      - xdr:rowOff
    - xdr:sp and xdr:cxnSp
      - xdr:nvSpPr(nvCxnSpPr)
        - xdr:cNvPr >> id, name | the id and name of the drawing
      - xdr:spPr
        - xdr:xfrm
          - xdr:off >> x, y | the position of the drawing (top-left corner)
          - xdr:ext >> cx, cy | the size of the drawing (width, height)
    - xdr:cxnSp
      - xdr:spPr
        - xdr:prstGeom >> prst | the drawing type name
        - xdr:ln >> w (cap, cmpd, algn are not parsed) | the line data
          - xdr:headEnd(tailEnd) >> type, w, len
          - xdr:prstDash >> val | the dash style
