import logging
from typing import Optional
import matplotlib.pyplot as plt
from .base_loader import BaseLoader
from spreadsheet_intelligence.read_data.excel_to_xml import (
    convert_xlsx_to_xml_in_memory,
)
from spreadsheet_intelligence.parsers.drawing.drawing_xml_parser import DrawingXMLParser
from spreadsheet_intelligence.parsers.theme.theme_xml_parser import ThemeXMLParser
from spreadsheet_intelligence.models.raw.drawing.drawing_models import (
    ConnectorAnchorRaw,
    ShapeAnchorRaw,
)
from spreadsheet_intelligence.models.raw.theme.theme_models import Theme
from spreadsheet_intelligence.models.common.enums import ConnectorType
from spreadsheet_intelligence.converters.drawing.drawing_raw_converters.connector_raw_converter import (
    StraightConnector1Converter,
    BentConnector3Converter,
)
from spreadsheet_intelligence.converters.drawing.drawing_raw_converters.shape_raw_converter import (
    ShapeConverter,
)
from spreadsheet_intelligence.models.converted.drawing_models import (
    StraightConnector1,
    BentConnector3,
    Shape,
)
from spreadsheet_intelligence.formatters.drawing.format import AllDrawingsFormatter

logger = logging.getLogger(__name__)


class ExcelAutoshapeLoader(BaseLoader):
    """
    A loader class for extracting and converting autoshapes from an Excel file.

    Attributes:
        file_path (str): Path to the Excel file.
        drawing_xml_path (str): Path to the drawing XML within the Excel file.
        theme_xml_path (str): Path to the theme XML within the Excel file.
        xml_contents (dict): In-memory XML contents of the specified files.
        drawing_root (Element): Root element of the drawing XML.
        theme_root (Element): Root element of the theme XML.
        connector_list (list[ConnectorAnchorRaw]): List of raw connector data.
        shape_list (list[ShapeAnchorRaw]): List of raw shape data.
        theme (Optional[Theme]): Parsed theme data.
        converted_connector_list (list[BentConnector3]): List of converted connectors.
        converted_shape_list (list[Shape]): List of converted shapes.
        id_counter (int): Counter for assigning unique IDs to converted elements.
    """

    def __init__(self, file_path: str):
        """
        Initializes the ExcelAutoshapeLoader with the given file path.

        Args:
            file_path (str): The path to the Excel file to be processed.
        """
        super().__init__(file_path)
        logger.debug(f"Initializing ExcelAutoshapeLoader with file_path: {file_path}")
        self.drawing_xml_path = "xl/drawings/drawing1.xml"
        self.theme_xml_path = "xl/theme/theme1.xml"
        self.xml_contents = convert_xlsx_to_xml_in_memory(
            file_path,
            target_files=[self.drawing_xml_path, self.theme_xml_path],
            out_dir="data/xml/flow_not_recurrent_group",
        )
        logger.info("XML contents successfully converted to in-memory structures.")

        self.drawing_root = self.xml_contents[self.drawing_xml_path]
        self.theme_root = self.xml_contents[self.theme_xml_path]

        # Lists to store parsed raw data
        self.connector_list: list[ConnectorAnchorRaw] = []
        self.shape_list: list[ShapeAnchorRaw] = []

        # Parsed theme data
        self.theme: Optional[Theme] = None

        # Lists to store converted data
        self.converted_connector_list: list[BentConnector3] = []
        self.converted_shape_list: list[Shape] = []
        self.id_counter = 1

    def _parse(self):
        """
        Parses the drawing and theme XML files to extract raw shape and connector data.
        """
        logger.debug("Starting parsing of XML contents.")
        try:
            # Parse drawing XML for shapes and connectors
            drawing_parser = DrawingXMLParser(self.drawing_root)
            self.connector_list, self.shape_list = drawing_parser.parse()
            logger.info(
                f"Parsed {len(self.connector_list)} connectors and {len(self.shape_list)} shapes from drawing XML."
            )

            # Parse theme XML for theme data
            theme_parser = ThemeXMLParser(self.theme_root)
            self.theme = theme_parser.parse()
            logger.info("Parsed theme information from theme XML.")
        except Exception as e:
            logger.error(f"Error during parsing: {e}", exc_info=True)
            raise

    def _convert(self):
        """
        Converts raw shape and connector data into structured objects.
        """
        logger.debug("Starting conversion of raw connectors and shapes.")
        try:
            for connector in self.connector_list:
                if (
                    connector.drawing.connector_type
                    == ConnectorType.STRAIGHT_CONNECTOR_1
                ):
                    # Convert straight connectors
                    converter = StraightConnector1Converter(
                        connector, self.theme, self.id_counter
                    )
                    converted = converter.convert()
                    self.converted_connector_list.append(converted)
                    self.id_counter += 1
                    logger.debug(f"Converted StraightConnector1: {converted}")
                elif connector.drawing.connector_type == ConnectorType.BENT_CONNECTOR_3:
                    # Convert bent connectors
                    converter = BentConnector3Converter(
                        connector, self.theme, self.id_counter
                    )
                    converted = converter.convert()
                    self.converted_connector_list.append(converted)
                    self.id_counter += 1
                    logger.debug(f"Converted BentConnector3: {converted}")
                else:
                    logger.warning(
                        f"Unsupported connector type: {connector.drawing.connector_type}"
                    )
                    raise ValueError(
                        f"Unsupported connector type: {connector.drawing.connector_type}"
                    )

            for shape in self.shape_list:
                # Convert shapes
                converter = ShapeConverter(shape, self.theme, self.id_counter)
                converted = converter.convert()
                self.converted_shape_list.append(converted)
                self.id_counter += 1
                logger.debug(f"Converted Shape: {converted}")

            logger.info(
                f"Converted {len(self.converted_connector_list)} connectors and {len(self.converted_shape_list)} shapes."
            )
        except Exception as e:
            logger.error(f"Error during conversion: {e}", exc_info=True)
            raise

    def _format(self):
        """
        Generates a prompt from the converted shapes and connectors.
        """
        logger.debug("Starting prompt generation.")
        try:
            formatters = AllDrawingsFormatter(
                self.converted_connector_list, self.converted_shape_list
            )
            self.prompt = formatters.format2json()
            logger.info("Prompt successfully generated.")
        except Exception as e:
            logger.error(f"Error during prompt generation: {e}", exc_info=True)
            raise

    def load(self):
        """
        Loads and processes the Excel autoshapes by parsing, converting, and generating prompts.
        """
        logger.info("Loading Excel autoshapes.")
        self._parse()
        self._convert()
        self._format()
        logger.info("Excel autoshapes loaded successfully.")

    def export(self) -> str:
        """
        Exports the generated prompt as a JSON string.

        Returns:
            str: The JSON string of the prompt.
        """
        logger.debug("Exporting prompt.")
        try:
            logger.info("Exporting prompt successfully.")
            return self.prompt
        except Exception as e:
            logger.error(f"Error during export: {e}", exc_info=True)
            raise

    def plot_for_debug(self):
        """
        Plots the converted shapes and connectors for debugging purposes.
        """
        fig, ax = plt.subplots()
        for shape in self.converted_shape_list:
            shape.plot(ax)
        for connector in self.converted_connector_list:
            connector.plot(ax)
        ax.invert_yaxis()
        save_path = "debug.png"
        plt.savefig(save_path)
        plt.close()
        logger.info(f"Plot saved to {save_path}")
