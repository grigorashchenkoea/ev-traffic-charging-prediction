# AGENTS.md

Repository-wide instructions for AI coding agents. Everything here applies
everywhere.

Directory-specific rules live in nested `AGENTS.md` files and *add* to this one
rather than replacing it:

- [`src/AGENTS.md`](src/AGENTS.md) — package code

Read the nested file for the directory you are editing. Claude Code 2.1.277+
reads this file directly. A `CLAUDE.md` exists only for rules that hold for
Claude Code alone and then opens with `@AGENTS.md`; the `sync-agent-context`
pre-commit hook repairs any other shape.

## Commands

```bash
uv sync                        # Install dependencies
uv run ruff check --fix        # Lint (run before format)
uv run ruff format             # Format
uv run ty check                # Type check
uv run pre-commit run --all-files
```

Always `uv run <cmd>` — never bare `python`, never `pip install` (use `uv add`).

## Mandates

- **No type suppression.** Never silence an error with `# type: ignore`,
  `# ty: ignore`, or `as any`. Fix the underlying type. If an ignore is truly
  unavoidable, use the rule-specific form `# ty: ignore[rule-name]`.
- **Lint before format.** `ruff check --fix` changes code structure;
  `ruff format` cleans up after it. The reverse order needs a second pass.
- **Scope fixes to files you touched.** Don't reformat or re-lint the whole
  codebase unasked.
- **Validate before claiming done.** Run lint, type check, and the code
  end-to-end, and report the actual output. Never assert something passes
  without running it.

## Working principles

### Think before coding

Don't assume, don't hide confusion, surface tradeoffs.

- State assumptions explicitly. If uncertain, ask.
- Multiple valid interpretations? Present them — don't pick silently.
- Simpler approach exists? Say so. Push back when warranted.

### Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No configurability that wasn't requested.
- No error handling for impossible scenarios.

Test: would a senior engineer call this overcomplicated?

### Surgical changes

Touch only what you must. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting.
- Match existing style even if you'd do it differently.
- Notice unrelated dead code? Mention it — don't delete it.
- Remove imports and variables that *your* change orphaned.

Every changed line should trace to the request.

### Goal-driven execution

Turn tasks into verifiable goals:

- "Add validation" → "Feed it invalid inputs, confirm they are rejected"
- "Fix the bug" → "Reproduce it first, confirm the run no longer shows it"
- "Refactor X" → "Output identical before and after"

For multi-step work, state the plan with a verification step per item.

### Testing regime

Default testing is end-to-end: run it and check the output is plausible.

## Agent memory

This file is the agents' permanent memory for this directory tree. Record a
finding or learning here when it would steer every future session — one or
two lines, in the section where it belongs. When a section outgrows a few
lines, relocate: directory-specific material into that directory's own
`AGENTS.md`, procedures only some tasks need into a skill. When memory
outgrows even that structure, suggest to the user creating a permanent
knowledge store (such as an `okf/` bundle) where full findings live and this
file keeps one-line lessons plus pointers. Prune stale lines on every edit.

## Git

- Atomic commits, one logical change each.
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.
- Never commit automatically — propose the message for review first.
- Attribute AI-assisted work:

```bash
git commit -m "feat: add user validation" -m "Generated-by: AI-Agent"
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and workflow details.
