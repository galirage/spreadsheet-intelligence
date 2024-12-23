import pytest
from spreadsheet_intelligence.converters.drawing.drawing_raw_converters.connector_raw_converter import (
    StraightConnector1Converter,
    BentConnector3Converter,
)
from spreadsheet_intelligence.models.raw.drawing.anchor_models import (
    Anchor,
    AnchorPoint,
)
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ConnectorAnchorRaw,
    ConnectorRaw,
    ArrowLine,
    ArrowHead,
)
from spreadsheet_intelligence.models.raw.theme.theme_models import (
    Theme,
    SrgbClr,
    SysClr,
)


@pytest.fixture
def sample_anchor():
    return Anchor(
        from_point=AnchorPoint(col=0, colOff=508000, row=6, rowOff=208753),
        to_point=AnchorPoint(col=13, colOff=359355, row=31, rowOff=27576),
    )


@pytest.fixture
def sample_straight_connector_1_anchor_raw(sample_anchor):
    connector_raw = ConnectorRaw(
        connector_type="straightConnector1",
        x=508000,
        y=208753,
        width=359355,
        height=27576,
        rotation=80,
        flip_h=True,
        flip_v=False,
        arrow_line=ArrowLine(
            width=1,
            cap="flat",
            compound="round",
            alignment="center",
            dash_style="solid",
            head=ArrowHead(type="triangle", width="medium", length="medium"),
            tail=ArrowHead(type="triangle", width="medium", length="medium"),
        ),
        interm_line_pos=None,
    )
    return ConnectorAnchorRaw(anchor=sample_anchor, drawing=connector_raw)


@pytest.fixture
def sample_bent_connector_3_anchor_raw(sample_anchor):
    connector_raw = ConnectorRaw(
        connector_type="bentConnector3",
        x=508000,
        y=208753,
        width=359355,
        height=27576,
        rotation=90 * 60000,
        flip_h=True,
        flip_v=False,
        arrow_line=ArrowLine(
            width=1,
            cap="flat",
            compound="round",
            alignment="center",
            dash_style="solid",
            head=ArrowHead(type="triangle", width="medium", length="medium"),
            tail=ArrowHead(type="triangle", width="medium", length="medium"),
        ),
        interm_line_pos=100,
    )
    return ConnectorAnchorRaw(anchor=sample_anchor, drawing=connector_raw)


def test_straight_connector_1_converter(sample_straight_connector_1_anchor_raw):
    converter = StraightConnector1Converter(sample_straight_connector_1_anchor_raw)
    sc_1 = converter.convert()
    print(sc_1)


def test_bent_connector_3_converter(sample_bent_connector_3_anchor_raw):
    converter = BentConnector3Converter(sample_bent_connector_3_anchor_raw)
    bc_3 = converter.convert()
    print(bc_3)
