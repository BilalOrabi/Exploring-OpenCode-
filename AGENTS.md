# AGENTS

## Project layout

| Path                    | Purpose                                                        |
| ----------------------- | -------------------------------------------------------------- |
| `sloperator.py`         | CLI: `uv run sloperator.py [--check] <file.slop>`              |
| `sloperator/lexer/`     | Source text to tokens                                          |
| `sloperator/parser/`    | Tokens to AST; parser conventions live in `parser/AGENTS.md`   |
| `sloperator/evaluator/` | Values, environments, and the tree-walking interpreter         |
| `sloperator/runner.py`  | Pipeline entry points; `run_source()` is the test seam         |
| `tests/`                | Pytest suite; every `examples/*.slop` is auto-tested           |
| `examples/`, `playground/` | Sample programs and the local web playground               |
| `docs/spec.md`          | The SlopLang language specification                            |

## Validation

Run from the repo root, in this order:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

After any code change, run the formatter first: `uv run ruff format` (then the checks above).

Narrower runs: `uv run pytest tests/test_parser.py -q`, `uv run pytest tests/test_parser.py::test_name -q`, or `uv run pytest tests/test_comparisons.py -q` for equality/comparison precedence tests.

## When to add regression tests

Add a test whenever you fix a bug or add/change a lexical, syntax, or runtime error path, especially one that previously had no coverage. Test through `sloperator.runner.run_source()` and assert the exact `SlopLang <kind> error at line N: <message>` string, including any stdout produced before the error. New `examples/*.slop` files become tests automatically, so they must exit 0 and print something.

## Language behavior

Read [docs/spec.md](docs/spec.md) for syntax, grammar, values, operators, scoping, and the error contract. Do not duplicate it into README, which must stay under 50 lines and link back to the spec.

Lesson checks: `bootdev run <id>` is the dry run. If it reports no failures, immediately submit with `bootdev run -s <id>` without asking. Run `bootdev upgrade` if the CLI demands a newer version.
