import pytest
from xml.etree.ElementTree import parse
from spreadsheet_intelligence.parsers.theme.theme_parser import ThemeParser


@pytest.fixture
def load_theme_xml():
    xml_path = "data/xml/arrow_ln_edited.xml/xl/theme/theme1.xml"
    tree = parse(xml_path)
    root = tree.getroot()
    return root


def test_parse_clr_scheme(load_theme_xml):
    root = load_theme_xml
    namespaces = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    clr_scheme_el = root.find(".//a:clrScheme", namespaces=namespaces)
    clr_scheme = ThemeParser(namespaces)._parse_clr_scheme(clr_scheme_el)
    print(clr_scheme)


def test_parse_theme(load_theme_xml):
    root = load_theme_xml
    namespaces = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    theme_el = root.find("a:themeElements", namespaces=namespaces)
    theme = ThemeParser(namespaces).parse(theme_el)
    print(theme)
