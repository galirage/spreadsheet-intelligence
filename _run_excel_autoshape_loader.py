from spreadsheet_intelligence.core import ExcelAutoshapeLoader


if __name__ == "__main__":
    loader = ExcelAutoshapeLoader("data/xlsx/flow_not_recurrent_group.xlsx")
    loader.load()
    diagram_json = loader.export()
    with open("data/json/diagram_json.json", "w") as f:
        f.write(diagram_json)
