import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("hallucinate(2 + 3 * 4)✨", "14\n"),
        ("hallucinate(2 * 3 + 4)✨", "10\n"),
        ("hallucinate(1 + 2 * 3 + 4 * 5)✨", "27\n"),
    ],
)
def test_multiplication_binds_tighter_than_addition(source: str, expected: str):
    result = run_source(source)
    assert result.stderr == "", result.stderr
    assert result.stdout == expected


def test_multiplication_is_nested_inside_addition_in_the_ast():
    (statement,) = parse(tokenize("2 + 3 * 4✨"))
    assert isinstance(statement, ExprStmt)

    addition = statement.expression
    assert isinstance(addition, Binary) and addition.operator.type is TokenType.PLUS
    assert isinstance(addition.left, Literal) and addition.left.value == 2

    product = addition.right
    assert isinstance(product, Binary) and product.operator.type is TokenType.STAR
    assert isinstance(product.left, Literal) and product.left.value == 3
    assert isinstance(product.right, Literal) and product.right.value == 4
