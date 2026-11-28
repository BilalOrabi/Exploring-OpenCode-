---
name: create-and-validate
description: Add a SlopLang example program and exact-output test, then run the full validation suite
---

# Create and Validate

Load these skills in order with the `skill` tool, using the exact IDs, and follow each one fully:

1. `create-test-program`
2. `validate`

This skill is only an orchestrator. It deliberately does not copy either skill's instructions — their bodies are the source of truth, so this workflow automatically follows any updates to them. Use each loaded skill's own base directory for its supporting files.

Report the combined result: the example path and expected output from `create-test-program`, followed by the check results from `validate`. If the first skill cannot complete, stop and report why instead of validating a partial change.
