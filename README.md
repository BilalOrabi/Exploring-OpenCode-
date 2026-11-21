# Sloperator

A tree-walking interpreter for SlopLang, written in Python.

```bash
uv run sloperator.py examples/fib.slop                  # run a program
uv run sloperator.py --check path/to/program.slop       # lex + parse only
```

Validation:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

The full language specification lives in [docs/spec.md](docs/spec.md).

## Example

```slop
— Comments start with an em dash. Statements end with sparkles.
slop count = 2✨
hallucinate(“count:”, count)✨
```

## Layout

| Path                    | What it is                                       |
| ----------------------- | ------------------------------------------------ |
| `sloperator.py`         | CLI entrypoint                                   |
| `sloperator/lexer/`     | Source text to tokens                            |
| `sloperator/parser/`    | Tokens to AST                                    |
| `sloperator/evaluator/` | Values, environments, the interpreter            |
| `sloperator/runner.py`  | Runs source through all stages                   |
| `docs/spec.md`          | Language specification                           |
| `examples/`, `tests/`   | Sample programs and the pytest suite             |
| `playground/`           | Tiny web server and editor for running programs  |

## Playground

```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.
