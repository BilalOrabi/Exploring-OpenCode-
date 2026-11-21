"""Tests for calls nested directly inside other calls' argument lists."""

from sloperator.runner import run_source


def test_call_used_directly_as_an_argument_to_another_call():
    source = """clanker double(n) {
    ship n * 2✨
}
clanker add_one(n) {
    ship n + 1✨
}
hallucinate(double(add_one(4)))✨"""
    result = run_source(source)

    assert (result.stdout, result.stderr, result.exit_code) == ("10\n", "", 0)
