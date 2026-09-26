# Basic Project Template

**Keywords**: Example, keyword

## Project Overview

This is an example project description, put yours here.

## Quick Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Install dependencies and set up environment
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

That's it! You're ready to start developing.

## Pre-commit Hooks

Pre-commit hooks are configured to run automated checks before each commit, when
they fail files need to be fixed, re-staged, and committed again. Some files are
also automatically formatted by the hooks, check for changes. The hooks can also
be run manually with `uv run pre-commit run --all-files`.

## Project Structure

```text
project/
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── .claude/settings.json     # Claude Code permission allowlist and the EnergyIT marketplace
├── .gitignore                # Git ignore rules
├── .python-version           # Python version pinning
├── pyproject.toml            # Project configuration and dependencies
├── README.md                 # This file
├── CONTRIBUTING.md           # Development guidelines
├── AGENTS.md                 # AI agent instructions (repo-wide)
├── CLAUDE.md                 # Symlink to AGENTS.md (Claude Code reads this)
└── src/                      # Source code
    ├── AGENTS.md             # Package-specific agent rules
    └── CLAUDE.md             # Symlink to src/AGENTS.md
```

Agent instructions are hierarchical: the root `AGENTS.md` always applies, and
each nested one adds only what is specific to its directory.

## Requirements

- Python 3.13+
- uv

## Quick Links

- **[Contributing Instructions](CONTRIBUTING.md)** - How to set up your environment and contribute

## Authors

- Your Name <your.email@example.com>
