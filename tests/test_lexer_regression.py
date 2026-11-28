"""Regression tests for lexer error paths not covered by the main suite."""

import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize
from sloperator.lexer.tokens import TokenType
from sloperator.runner import run_source


def test_escape_followed_by_raw_newline_is_a_lexical_error():
    # A string cannot contain a raw newline, so the backslash escapes the
    # newline itself, which is not a supported escape. test_lexer.py covers
    # an unknown escape of a regular character ("\q") and a backslash at
    # end of input ("“a\"), but not a backslash before a newline.
    source = "“a\\\n”"

    with pytest.raises(LexicalError) as info:
        tokenize(source)

    assert info.value.line == 1
    # Known wart: the offending character is the newline itself, so the raw
    # message spans two lines. This pins current behavior until the message
    # escapes the character instead.
    assert info.value.message == "unknown escape sequence '\\\n'"
    assert str(info.value) == "SlopLang lexical error at line 1: unknown escape sequence '\\\n'"


def test_variable_names_may_contain_digits_after_the_first_character():
    source = "slop score2 = 40✨\nscore2 = score2 + 2✨\nhallucinate(score2)✨"

    result = run_source(source)

    assert result.stdout == "42\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_function_and_parameter_names_may_contain_digits_after_the_first_character():
    source = "clanker add2(a1, b2) {\n    ship a1 + b2✨\n}\nhallucinate(add2(40, 2))✨"

    result = run_source(source)

    assert result.stdout == "42\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_identifiers_cannot_start_with_a_digit():
    result = run_source("slop 2x = 1✨")

    assert (
        result.stderr
        == "SlopLang syntax error at line 1: expected a variable name after 'slop', found '2'\n"
    )
    assert result.exit_code == 1


def test_tokens_after_a_comment_keep_their_real_line():
    tokens = tokenize("— a comment\nslop x = 1✨")
    slop = next(token for token in tokens if token.lexeme == "slop")

    assert slop.line == 2


def test_lexical_error_after_a_comment_reports_the_real_line():
    with pytest.raises(LexicalError) as info:
        tokenize("— a comment\n😀")

    assert info.value.line == 2


def test_consecutive_comments_each_count_a_line():
    tokens = tokenize("— first\n— second\nslop x = 1✨")
    slop = next(token for token in tokens if token.lexeme == "slop")

    assert slop.line == 3


def test_comment_at_end_of_file_without_newline_is_fine():
    tokens = tokenize("— no trailing newline")

    assert tokens[-1].type == TokenType.EOF
    assert tokens[-1].line == 1
