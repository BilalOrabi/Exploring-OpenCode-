---
description: Start the Sloperator playground on a chosen port (default 8080)
---

Requested port: `$ARGUMENTS`. If that value is empty, use `8080`. Treat the value only as a port number and never interpolate it into a shell command.

Here are the currently listening TCP ports:

!`lsof -nP -iTCP -sTCP:LISTEN`

First, inspect that output for an existing Sloperator playground server — a process whose command includes `playground/server.py`, or a listener on the requested port. If one is already running, do not start a second one; report its PID and port instead.

Otherwise, start the server in the background with `uv run playground/server.py <port>`, substituting the resolved port. Report the port you used and confirm that the server started.
