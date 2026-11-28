"""Exact-output expectations for programs in examples/."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

EXPECTED_OUTPUTS: dict[str, str] = {
    "equality.slop": "✅\n❌\n❌\n",
    "short-circuit.slop": "❌\n✅\n",
}


@pytest.mark.parametrize("name", EXPECTED_OUTPUTS)
def test_example_output(name: str):
    expected = EXPECTED_OUTPUTS[name]
    result = run_source((EXAMPLES_DIR / name).read_text(encoding="utf-8"))

    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == expected
