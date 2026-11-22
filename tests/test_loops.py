"""Regression tests for ralph loops."""

from sloperator.runner import run_source


def test_loop_does_not_run_when_the_condition_is_false_initially():
    result = run_source(
        """ralph ❌ {
    hallucinate(“never”)✨
}"""
    )

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == ""
