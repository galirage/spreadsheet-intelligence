import pytest


def test_load():
    import os
    from spreadsheet_intelligence.core.excel_autoshape_loader import (
        ExcelAutoshapeLoader,
    )

    # f_path = "data/xlsx/bentarrow_direction.xlsx"
    f_path = "data/xlsx/flow_not_recurrent_group.xlsx"
    loader = ExcelAutoshapeLoader(f_path)
    loader.load()

    if not os.path.exists("data/json"):
        os.makedirs("data/json")
    with open("data/json/flow_not_recurrent_group.json", "w") as f:
        f.write(loader.export())
    loader.plot_for_debug()
