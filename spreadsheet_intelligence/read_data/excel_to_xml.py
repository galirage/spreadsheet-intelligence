import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
from io import BytesIO


def convert_xlsx_to_xml_in_memory(
    xlsx_path: str,
    target_files: Optional[List[str]] = None,
    out_dir: Optional[str] = None,
) -> Dict[str, ET.Element]:
    """Convert Excel file to XML format and process it in memory

    Args:
        xlsx_path (str): Path to the target Excel file
        target_files (Optional[List[str]]): List of target XML file names (to load only the necessary files to reduce memory usage), default is all XML files

    Returns:
        Dict[str, ET.Element]: Dictionary with XML file names as keys and corresponding XML Elements as values
    """
    xml_contents = {}
    with zipfile.ZipFile(xlsx_path, "r") as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith(".xml") and (
                target_files is None or file_info.filename in target_files
            ):
                with zip_ref.open(file_info) as file:
                    xml_data = file.read()
                    xml_tree = ET.parse(BytesIO(xml_data))
                    xml_root = xml_tree.getroot()
                    xml_contents[file_info.filename] = xml_root
    if out_dir is not None:
        convert_xlsx_to_xml(xlsx_path, out_dir)
    return xml_contents


def convert_xlsx_to_xml(xlsx_path: str, xml_dir: str) -> None:
    """Convert Excel file to XML format

    Args:
        xlsx_path (str): Path to the target Excel file
        xml_dir (str): Directory to output the XML format
    """
    with zipfile.ZipFile(xlsx_path, "r") as zip_ref:
        zip_ref.extractall(xml_dir)
