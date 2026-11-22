---
name: create-test-program
description: Add a SlopLang example program and exact-output test for a language feature
---

# Create Test Program

Use this when asked to cover a SlopLang language feature with an example program and an exact-output test.

## Steps

1. Read `docs/spec.md` and find the section covering the feature. Confirm its syntax, semantics, output, and any error behavior before writing code. Do not guess at behavior the spec does not describe.
2. Add a program at `examples/<feature>.slop` that demonstrates the feature. Follow the style of the existing examples:
   - Use the Slop words (`slop`, `clanker`, `vibe`, `nah`, `ralph`, `hallucinate`, `ship`) and emoji tokens (`✨`, `✅`, `❌`).
   - Use curly quotes (`“ ”`) for strings and an em-dash (`—`) for comments.
   - Keep output deterministic, print at least one non-empty line, and exit 0.
   - It must pass `tests/test_examples.py`, which auto-discovers every `examples/*.slop`.
3. Add an exact-output case to `tests/test_example_outputs.py`. If the file does not exist, create it with this harness:

   ```python
   """Exact-output expectations for programs in examples/."""

   from pathlib import Path

   import pytest

   from sloperator.runner import run_source

   EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

   EXPECTED_OUTPUTS: dict[str, str] = {
       # "feature.slop": "expected output\n",
   }


   @pytest.mark.parametrize("name", EXPECTED_OUTPUTS)
   def test_example_output(name: str):
       expected = EXPECTED_OUTPUTS[name]
       result = run_source((EXAMPLES_DIR / name).read_text(encoding="utf-8"))

       assert result.stderr == ""
       assert result.exit_code == 0
       assert result.stdout == expected
   ```

   Add one entry keyed by the example's filename, with the exact stdout including trailing newlines. Run `uv run sloperator.py examples/<feature>.slop` first and copy its output rather than writing the expectation from memory; use `od -c` when trailing whitespace is unclear.
4. Run `uv run ruff format` after any code change, then validate:
   - `uv run pytest tests/test_example_outputs.py -q`
   - the full validation suite: `uv run pytest`, `uv run ruff format --check`, `uv run ruff check`, `uv run ty check`
5. Review the result: confirm the new example has exactly one matching entry in `EXPECTED_OUTPUTS`, the parametrized test id reads as the example filename, and no unrelated expectations changed.

Report the example path, the expected output, and which checks passed. If the feature's behavior contradicts `docs/spec.md`, report the mismatch instead of encoding the current behavior as expected.
