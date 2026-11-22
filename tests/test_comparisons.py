"""Regression tests for equality/comparison precedence.

`==` and `!=` bind looser than `<`, `<=`, `>`, and `>=`, so `1 < 2 == ✅`
parses as `(1 < 2) == ✅` and prints `✅`.
"""

import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt
from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 < 2 == ✅", "✅"),
        ("2 < 1 == ❌", "✅"),
        ("1 < 2 != ❌", "✅"),
        ("✅ == 1 < 2", "✅"),
    ],
)
def test_equality_binds_looser_than_comparison(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")

    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == f"{expected}\n"


def test_comparison_is_nested_inside_equality_in_the_ast():
    (statement,) = parse(tokenize("1 < 2 == ✅✨"))
    assert isinstance(statement, ExprStmt)

    equality = statement.expression
    assert isinstance(equality, Binary) and equality.operator.type is TokenType.EQUAL_EQUAL

    comparison = equality.left
    assert isinstance(comparison, Binary) and comparison.operator.type is TokenType.LESS
