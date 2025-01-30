.. spreadsheet-intelligence documentation master file, created by
   sphinx-quickstart on Mon Dec 23 13:52:22 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

🔭📊 spreadsheet-intelligence
=============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT



🤔 What is Spreadsheet Intelligence?
-------------------------------------

**Spreadsheet Intelligence** parses the XML of Excel files to load various data and enhance the RAG performance of Excel files using LLM.

Currently, it supports the conversion of system configuration diagrams consisting of autoshapes in Excel, and it is a powerful tool reported in our paper to overcome the limitations of VLM in diagram interpretation.

{論文ブックマーク埋め込み}

⚡️ Quick Install
--------------------------------------

With pip (coming soon):

.. code-block:: bash

   pip install spreadsheet_intelligence

🚀 Quick Start
----------------------------------------

Extract autoshape information from Excel and convert it to JSON format.
.. code-block:: python

   from spreadsheet_intelligence.core.excel_autoshape_loader import ExcelAutoshapeLoader

   loader = ExcelAutoshapeLoader(file_path="path/to/your/excel/file.xlsx")
   loader.load()
   autoshape_info_json = loader.export2json()
   print(autoshape_info_json)

Output example:

.. code-block:: json

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
           }
       ]
   }

🗂️ Project Structure
---------------------

This package is mainly composed of the following 5 packages:

.. code-block:: text

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

🔥 Processing Flow
------------------

The Excel file loaded as XML is processed in the following flow:

1. It is parsed by ``parsers`` in a nearly raw state and stored in ``Raw`` models.
2. It is converted by ``converters`` from the XML representation to a structure that is easy for humans (LLM) to understand and stored in ``Converted`` models.
3. It is converted by ``formatters`` from the ``Converted`` models to JSON format data that can be directly used in LLM prompts.

Basically, by using the ``ExcelAutoshapeLoader`` class in the ``core`` package, this flow can be wrapped and executed.


🔧 Customizability
------------------

Mainly extendable in the following ways:

- Extend the data retrieved from XML -> Extend by inheriting from ``parsers``  
- Extend the data conversion methods -> Extend by inheriting from ``converters``  
- Extend the output data format -> Extend by inheriting from ``formatters``  
