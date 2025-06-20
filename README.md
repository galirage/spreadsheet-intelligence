<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

![logo](https://raw.githubusercontent.com/galirage/spreadsheet-intelligence/main/assets/galirage_logo.png)

# 🔭📊 Spreadsheet Intelligence

[![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![API Reference](https://img.shields.io/badge/API-Reference-blue)](https://galirage.github.io/spreadsheet-intelligence/)
[![PyPI version](https://img.shields.io/pypi/v/your-package-name.svg)](https://pypi.org/project/spreadsheet-intelligence/)

## ⚡ Quick Install

With pip:

```bash
pip install spreadsheet_intelligence
```

## 🤔 What is Spreadsheet Intelligence?
**Spreadsheet Intelligence** parses the XML of Excel files to load various data and enhance the RAG performance of Excel files using LLM.

Currently, it supports the conversion of system configuration diagrams consisting of autoshapes in Excel, and it is a powerful tool reported in our paper to overcome the limitations of VLM in diagram interpretation.

The paper is available on arXiv.

[![arXiv](https://img.shields.io/badge/arXiv-2502.04389-blue.svg)](https://arxiv.org/abs/2502.04389)
[![Static Badge](https://img.shields.io/badge/Github-XMLDriven--Diagram--Understanding-blue?logo=github)](https://github.com/galirage/XMLDriven-Diagram-Understanding)

## 🚀 Quick Start
```python
from spreadsheet_intelligence.core.excel_autoshape_loader import ExcelAutoshapeLoader

loader = ExcelAutoshapeLoader(file_path="path/to/your/excel/file.xlsx")
loader.load()
autoshape_info_json = loader.export2json()
print(autoshape_info_json)
```
The output is as follows
```
{
    "connectors": [
        {
            "type": "straightConnector1",
            "arrowType": "bidirectional",
            "color": "#000000",
            "startX": "8.47",
            "startY": "8.77",
            "endX": "18.30",
            "endY": "8.77"
        },
        {
            "type": "bentConnector3",
            "arrowType": "unidirectional",
            "color": "#000000",
            "startX": "14.75",
            "startY": "4.74",
            "StartArrowHeadDirection": "left",
            "endX": "21.59",
            "endY": "6.00",
            "EndArrowHeadDirection": "right"
        }
        ...
    ],
    "shapes": [
        {
            "shapeType": "round_rect",
            "fillColor": "#156082",
            "borderColor": "#0E2841",
            "left": "1.41",
            "top": "5.52",
            "right": "39.13",
            "bottom": "23.40",
            "text": null
        },
        {
            "shapeType": "rect",
            "fillColor": "#000000",
            "borderColor": "#000000",
            "left": "5.17",
            "top": "19.07",
            "right": "9.27",
            "bottom": "19.87",
            "text": {
                "content": "Azure Cognitive Search",
                "fontColor": null,
                "fontSize": null,
                "alignment": null
            }
        },
        ...
    ]
}

```

## 🗂️ Project Structure
This package is mainly composed of five packages: core, models, parsers, converters, and formatters.
```
spreadsheet_intelligence/
├── core/
│   ├── excel_autoshape_loader.py
├── models/
│   ├── converted/
│   ├── raw/
├── parsers/
├── converters/
├── formatters/
├── ...
```

### Basic Processing Flow
The Excel file loaded as XML is processed in the following flow:
1. It is parsed by `parsers` in a nearly raw state and stored in `Raw` models.
2. It is converted by `converters` from the XML representation to a structure that is easy for humans (LLM) to understand and stored in `Converted` models.
3. It is converted by `formatters` from the `Converted` models to JSON format data that can be directly used in LLM prompts.

Basically, by using the `ExcelAutoshapeLoader` class in the `core` package, this flow can be wrapped and executed.

### Customizability
Mainly extendable in the following ways:
- Extend the data retrieved from XML -> Extend by inheriting from `parsers`
- Extend the data conversion methods -> Extend by inheriting from `converters`
- Extend the output data format -> Extend by inheriting from `formatters`
