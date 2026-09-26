# Contributing Guide

## Project Philosophy

This template is a **starting point**, not a fixed requirement. Remove tools you
don't need, loosen ruff rules that are too strict for your use case, add tools
for larger projects. Adapt it to your workflow.

## Prerequisites

- **Python** 3.13+ (managed by `uv`)
- **uv** — package management and tool execution
- **git** — version control

## Setup

```bash
git clone <your-repo-url>
cd <your-repo-name>

uv sync                  # Install dependencies
uv run pre-commit install # Install git hooks
```

## Pre-commit Hooks

Hooks run automatically before each commit:

- Merge conflict markers, YAML/TOML syntax, large file detection, destroyed
  symlinks
- `sync-agent-context` — keeps `CLAUDE.md` a symlink to `AGENTS.md` (from the
  EnergyIT Claude marketplace, see [For AI Agents](#for-ai-agents))
- `ruff check --fix` — linting
- `ruff format` — formatting
- `ty check` — type checking
- `pymarkdown scan` — markdown linting

Some hooks modify files. When a hook fails, fix or re-stage the changes and
commit again. Run them manually with `uv run pre-commit run --all-files`.

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run `uv run pre-commit run --all-files`
4. Commit and push

## Technical Conventions

### Python

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- Type hints on all function signatures
- Docstrings for public functions and classes
- Max cyclomatic complexity: 15

### Testing

Default testing is end-to-end: run the code and check the output is plausible.
For a project that needs unit tests, add pytest (`uv add --dev pytest`) and
place them in `tests/`, named for the behaviour they assert.

### Git

- Atomic, logical commits
- Conventional Commits format, imperative mood
- One feature or fix per branch

### Security

- Never commit secrets or API keys
- Use environment variables for sensitive configuration
- `.env` files stay in `.gitignore`

## Git LFS (Optional)

Only needed if you commit datasets, ML models, or media. **Most projects don't.**

Install from <https://git-lfs.com/>, then:

```bash
git lfs install
git lfs track "*.csv"        # Track a file type
git add .gitattributes
```

Use it only for files over ~100KB.

## For AI Agents

Agent instructions live in [AGENTS.md](AGENTS.md) at the repo root — commands,
mandates, and working principles.

**Claude Code does not read `AGENTS.md`.** It reads `CLAUDE.md`, which this repo
provides as a symlink:

```bash
ln -s AGENTS.md CLAUDE.md
```

On Windows, symlinks need Administrator privileges or Developer Mode. If that's
a problem, replace the symlink with a real `CLAUDE.md` whose entire contents are
the line `@AGENTS.md` — Claude Code expands that import at session start.

**`CLAUDE.md` must never hold instructions of its own.** Anything written there
is invisible to every agent that reads `AGENTS.md`, which forks the source of
truth. The `sync-agent-context` pre-commit hook (from the EnergyIT Claude
marketplace, pinned by tag in `.pre-commit-config.yaml`) maintains this: it
creates a missing `CLAUDE.md` symlink beside every `AGENTS.md`, repoints or
repairs a broken one, and merges back content that diverged — failing the
commit so you review what it changed. This applies to nested `AGENTS.md` files
in subdirectories too.

Verify it loaded: run `/context` in a session and check **Memory files**.

### Hierarchy

Instructions are split by scope so agents carry only what's relevant:

| File | Scope |
| ---- | ----- |
| `AGENTS.md` | Repo-wide — always applies |
| `src/AGENTS.md` | Package code: docstrings, annotations, security lints |

Nested files *add* to the root, never replace it. Claude Code loads a nested
file on demand when it reads a file in that directory, so subdirectory rules
cost no context until they're needed. Add another for any module that grows its
own conventions — remember the paired `CLAUDE.md` symlink, or the hook fails.

For procedures rather than facts (multi-step workflows, checklists), write a
[skill](https://code.claude.com/docs/en/skills) at
`.claude/skills/<name>/SKILL.md`. Skill bodies load only when invoked, so long
reference material costs nothing until it's needed.

`SKILL.md` is the [Agent Skills](https://agentskills.io) open standard, and
`.claude/skills/` is not Claude-only: OpenCode scans that path too, so one copy
serves both. Claude-specific frontmatter (`allowed-tools`, `when_to_use`) is
ignored rather than rejected by other tools — portable, but don't rely on it
for behaviour that matters outside Claude Code.

Before writing a skill, check the
[EnergyIT Claude marketplace](https://gitlab.tuwien.ac.at/energyit_projects/internal/tools/energyit-claude-marketplace):
the group's shared skills, agents, and gate hooks live there as plugins.
`.claude/settings.json` already declares the marketplace, so enabling a plugin
is one `enabledPlugins` entry — see the marketplace README for the catalog.

For advanced multi-agent infrastructure (Plan → Act → Validate cycle,
specialized agents, automated validation reporting):

→ [Agentic Coding Standards Template](https://gitlab.tuwien.ac.at/energyit_projects/internal/tools/agentic-coding-standards)

For writing projects:

→ [Agentic Writing Standards Template](https://gitlab.tuwien.ac.at/energyit_projects/internal/tools/agentic-writing-standards)
