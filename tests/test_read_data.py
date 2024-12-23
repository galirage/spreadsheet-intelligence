import pytest
from pympler import asizeof


@pytest.fixture
def xlsx_path():
    return "./data/xlsx/flow_not_recurrent_group.xlsx"


def test_convert_xlsx_to_xml_in_memory(xlsx_path):
    from spreadsheet_intelligence.read_data.excel_to_xml import (
        convert_xlsx_to_xml_in_memory,
    )
    import xml.etree.ElementTree as ET

    xml_contents = convert_xlsx_to_xml_in_memory(xlsx_path)

    assert isinstance(xml_contents, dict)
    assert len(xml_contents) > 0

    assert "xl/drawings/drawing1.xml" in xml_contents
    assert "xl/theme/theme1.xml" in xml_contents

    for filename, xml_root in xml_contents.items():
        assert filename.endswith(".xml")
        assert isinstance(xml_root, ET.Element)
        assert xml_root.tag is not None
        memory_size = asizeof.asizeof(xml_root)
        print(
            f"Filename: {filename}, Root Tag: {xml_root.tag}, Size: {memory_size} bytes"
        )
