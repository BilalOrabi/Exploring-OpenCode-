"""Regression tests for unary minus applied to non-number values."""

import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize("literal", ["✅", "❌"])
def test_unary_minus_rejects_booleans(literal: str):
    # The error is reported at the operator's line, and no output is produced.
    result = run_source(f"hallucinate(-\n    {literal})✨")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean\n"
    )
