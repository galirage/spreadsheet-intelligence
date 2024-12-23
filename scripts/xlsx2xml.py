import sys

sys.path.append(
    "/Users/shue/projects/excel2xml-rag/research_and_development/shiinoki_package"
)
import click
import os
from spreadsheet_intelligence.read_data.excel_to_xml import convert_xlsx_to_xml


@click.command()
@click.argument("xlsx_path", type=click.Path(exists=True))
@click.argument("xml_path", type=click.Path(), required=False)
def main(xlsx_path, xml_path=None):
    """Convert XLSX file to XML."""
    if xml_path is None:
        base_name = os.path.splitext(os.path.basename(xlsx_path))[0]
        xml_path = os.path.join("data/xml", f"{base_name}.xml")
    convert_xlsx_to_xml(xlsx_path, xml_path)


if __name__ == "__main__":
    main()
