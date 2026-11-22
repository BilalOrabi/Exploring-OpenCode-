# Parser conventions

- **One method per grammar rule.** Each rule in the grammar in `docs/spec.md` has exactly one `Parser` method. A method may call other rule methods, but it must own its whole rule: do not split a rule's loop or tail into a second method (for example, `factor` owns the `*`/`/` loop itself).
- **Syntax errors describe the token that was found.** Raise through `self.error(token, "...")` so every diagnostic ends in `, found '<lexeme>'` (or `, but reached end of file` at EOF). Never emit a bare "expected X" without saying what appeared instead.
