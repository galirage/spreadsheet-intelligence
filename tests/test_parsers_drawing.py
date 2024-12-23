# test_shape_parser.py
import pytest
import xml.etree.ElementTree as ET
from spreadsheet_intelligence.parsers.drawing.drawing_element_parser.shape_parser import (
    ShapeParser,
)
from spreadsheet_intelligence.parsers.drawing.drawing_element_parser.connector_parser import (
    ConnectorParser,
)
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ConnectorAnchorRaw,
    ShapeAnchorRaw,
)
from spreadsheet_intelligence.models.common.enums import ConnectorType


namespaces = {
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


@pytest.fixture
def sample_xmls():
    sp_xml_content = """
    <xdr:twoCellAnchor xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <xdr:from>
            <xdr:col>0</xdr:col>
            <xdr:colOff>508000</xdr:colOff>
            <xdr:row>6</xdr:row>
            <xdr:rowOff>208753</xdr:rowOff>
        </xdr:from>
        <xdr:to>
            <xdr:col>13</xdr:col>
            <xdr:colOff>359355</xdr:colOff>
            <xdr:row>31</xdr:row>
            <xdr:rowOff>27576</xdr:rowOff>
        </xdr:to>
        <xdr:sp>
            <xdr:nvSpPr>
                <xdr:cNvPr id="64" name="角丸四角形 63">
                    <a:extLst>
                        <a:ext uri="{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}">
                            <a16:creationId
                                xmlns:a16="http://schemas.microsoft.com/office/drawing/2014/main"
                                id="{90086CA9-F137-8645-8C87-FC94F23A5278}" />
                        </a:ext>
                    </a:extLst>
                </xdr:cNvPr>
                <xdr:cNvSpPr />
            </xdr:nvSpPr>
            
            <xdr:spPr>
                <a:xfrm flipH="1" flipV="1">
                    <a:off x="100" y="200"/>
                    <a:ext cx="300" cy="400"/>
                </a:xfrm>
                <a:prstGeom prst="ellipse"/>
                <a:ln>
                    <a:solidFill>
                        <a:schemeClr val="accent1"/>
                    </a:solidFill>
                </a:ln>
                <a:solidFill>
                    <a:schemeClr val="accent2"/>
                </a:solidFill>
            </xdr:spPr>
            <xdr:style>
                <a:lnRef idx="0">
                    <a:schemeClr val="accent1" />
                </a:lnRef>
                <a:fillRef idx="0">
                    <a:schemeClr val="accent1" />
                </a:fillRef>
                <a:effectRef idx="0">
                    <a:schemeClr val="accent1" />
                </a:effectRef>
                <a:fontRef idx="minor">
                    <a:schemeClr val="tx1" />
                </a:fontRef>
            </xdr:style>
            <xdr:txBody>
                <a:bodyPr wrap="square" rtlCol="0" anchor="t" />
                <a:lstStyle>
                    <a:defPPr>
                        <a:defRPr lang="ja-JP" />
                    </a:defPPr>
                    <a:lvl1pPr marL="0" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl1pPr>
                    <a:lvl2pPr marL="457200" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl2pPr>
                    <a:lvl3pPr marL="914400" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl3pPr>
                    <a:lvl4pPr marL="1371600" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl4pPr>
                    <a:lvl5pPr marL="1828800" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl5pPr>
                    <a:lvl6pPr marL="2286000" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl6pPr>
                    <a:lvl7pPr marL="2743200" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl7pPr>
                    <a:lvl8pPr marL="3200400" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl8pPr>
                    <a:lvl9pPr marL="3657600" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1"
                        latinLnBrk="0" hangingPunct="1">
                        <a:defRPr kumimoji="1" sz="1800" kern="1200">
                            <a:solidFill>
                                <a:schemeClr val="dk1" />
                            </a:solidFill>
                            <a:latin typeface="+mn-lt" />
                            <a:ea typeface="+mn-ea" />
                            <a:cs typeface="+mn-cs" />
                        </a:defRPr>
                    </a:lvl9pPr>
                </a:lstStyle>
                <a:p>
                    <a:pPr algn="ctr" />
                    <a:r>
                        <a:rPr kumimoji="1" lang="en-US" altLang="ja-JP" sz="1100" b="0" kern="1200">
                            <a:solidFill>
                                <a:sysClr val="windowText" lastClr="000000" />
                            </a:solidFill>
                        </a:rPr>
                        <a:t>Azure AI Document Intelligence</a:t>
                    </a:r>
                    <a:endParaRPr kumimoji="1" lang="ja-JP" altLang="en-US" sz="1100" b="0"
                        kern="1200">
                        <a:solidFill>
                            <a:sysClr val="windowText" lastClr="000000" />
                        </a:solidFill>
                    </a:endParaRPr>
                </a:p>
            </xdr:txBody>
        </xdr:sp>
    </xdr:twoCellAnchor>
    """
    connector_xml_content = """
    <xdr:twoCellAnchor xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <xdr:from>
            <xdr:col>0</xdr:col>
            <xdr:colOff>508000</xdr:colOff>
            <xdr:row>6</xdr:row>
            <xdr:rowOff>208753</xdr:rowOff>
        </xdr:from>
        <xdr:to>
            <xdr:col>13</xdr:col>
            <xdr:colOff>359355</xdr:colOff>
            <xdr:row>31</xdr:row>
            <xdr:rowOff>27576</xdr:rowOff>
        </xdr:to>
        <xdr:cxnSp macro="">
            <xdr:nvCxnSpPr>
                <xdr:cNvPr id="17" name="直線矢印コネクタ 16">
                        <a:extLst>
                            <a:ext uri="{FF2B5EF4-FFF2-40B4-BE49-F238E27FC236}">
                                <a16:creationId
                                    xmlns:a16="http://schemas.microsoft.com/office/drawing/2014/main"
                                    id="{C2621D96-873C-4888-517C-3D0E05887512}" />
                            </a:ext>
                        </a:extLst>
                </xdr:cNvPr>
                <xdr:cNvCxnSpPr />
            </xdr:nvCxnSpPr>
            <xdr:spPr>
                <a:xfrm flipH="1" flipV="1">
                        <a:off x="3050850" y="3155942" />
                        <a:ext cx="3539412" cy="0" />
                </a:xfrm>
                <a:prstGeom prst="straightConnector1">
                    <a:avLst />
                </a:prstGeom>
                <a:ln w="31750" cap="flat" cmpd="sng" algn="ctr">
                    <a:solidFill>
                        <a:schemeClr val="tx1" />
                    </a:solidFill>
                    <a:prstDash val="dash" />
                    <a:round />
                    <a:headEnd type="arrow" w="med" len="med" />
                    <a:tailEnd type="arrow" w="med" len="med" />
                </a:ln>
            </xdr:spPr>
            <xdr:style>
                <a:lnRef idx="0">
                    <a:schemeClr val="accent1" />
                </a:lnRef>
                <a:fillRef idx="0">
                    <a:schemeClr val="accent1" />
                </a:fillRef>
                <a:effectRef idx="0">
                    <a:schemeClr val="accent1" />
                </a:effectRef>
                <a:fontRef idx="minor">
                    <a:schemeClr val="tx1" />
                </a:fontRef>
            </xdr:style>
        </xdr:cxnSp>
    </xdr:twoCellAnchor>
    """
    return ET.fromstring(sp_xml_content), ET.fromstring(connector_xml_content)


def test_shape_parser(sample_xmls):
    sp_xml, connector_xml = sample_xmls

    parser = ShapeParser(namespaces)
    shape_element = parser.parse(sp_xml)
    print("\nshape_element: ", shape_element)
    assert isinstance(shape_element, ShapeAnchorRaw)
    shape_raw = shape_element.drawing


def test_connector_parser(sample_xmls):
    sp_xml, connector_xml = sample_xmls
    parser = ConnectorParser(namespaces)
    cn_anchor_raw = parser.parse(connector_xml)

    assert isinstance(cn_anchor_raw, ConnectorAnchorRaw)
    print("\ncn_anchor_raw: ", cn_anchor_raw)
    assert cn_anchor_raw.drawing.flip_h == True
    assert cn_anchor_raw.drawing.flip_v == True
