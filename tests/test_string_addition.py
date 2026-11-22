"""Regression tests for string addition with empty and Unicode operands."""

import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“” + “slop”", "slop"),
        ("“slop” + “”", "slop"),
        ("“” + “”", ""),
        ("“café” + “✨”", "café✨"),
    ],
)
def test_string_addition(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")

    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == f"{expected}\n"
