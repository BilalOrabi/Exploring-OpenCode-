import { Plugin } from "@opencode/plugin"
import { execFile } from "node:child_process"

type RunSlopResult = {
  stdout: string
  stderr: string
  exitCode: number
}

const MAX_OUTPUT_BYTES = 10 * 1024 * 1024

function runSloperator(directory: string, file: string, signal: AbortSignal): Promise<RunSlopResult> {
  return new Promise((resolve, reject) => {
    execFile(
      "uv",
      ["run", "--no-active", "sloperator.py", file],
      { cwd: directory, signal, maxBuffer: MAX_OUTPUT_BYTES },
      (error, stdout, stderr) => {
        // A numeric code means the process ran and exited non-zero; anything
        // else (e.g. ENOENT) means it never started.
        if (error && typeof error.code !== "number") {
          reject(error)
          return
        }
        resolve({
          stdout,
          stderr,
          exitCode: error ? (error.code as number) : 0,
        })
      },
    )
  })
}

export default Plugin.define({
  id: "run-slop",
  async setup(ctx) {
    const directory = ctx.location.directory

    await ctx.tool.transform((editor) => {
      editor.add({
        name: "run_slop",
        description:
          "Run a SlopLang program with the Sloperator interpreter (uv run --no-active sloperator.py <path>) from the project root and return stdout, stderr, and exitCode as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, relative to the project root or absolute",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async ({ path }, context) => {
          const result = await runSloperator(directory, path, context.signal)
          return { content: JSON.stringify(result) }
        },
      })
    })
  },
})
