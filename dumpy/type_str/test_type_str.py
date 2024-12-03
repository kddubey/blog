"""
Unit tests type_str
"""
import pandas as pd

from type_str import type_str


def test_type_str():
    df = pd.DataFrame(
        {
            "A": [0, 1],
            "B": ["hoo", "ha"],
            "C": [{"zero": 0, "one": 1}, {"two": 2, "three": 3}],
            "D": [[None, "hoo"], ["ha"]],
        }
    )  ## Postgres nulls are Python Nones
    column_types = df.apply(type_str)
    expected_column_types = pd.Series(
        {
            "A": "int",
            "B": "str",
            "C": "dict[str, int]",
            "D": "list[None | str] | list[str]",
        }
    )
    assert (column_types == expected_column_types).all()
