import pytest

from spreadsheet_intelligence.utils.helpers import apply_flip, apply_rotation


def test_apply_rotation():
    assert apply_rotation((1, 0), (0, 0), -90) == (0, 1)
