# AGENTS.md — package code

Applies to everything under `src/`. The [root AGENTS.md](../AGENTS.md) still
applies; this file only adds what is specific to the package.

## Layout

Package code lives in `src/your_package_name/`. The import name is
`your_package_name`, set in `[tool.hatch.build.targets.wheel]` — rename both
together or the wheel builds empty.

## Rules enforced here

- **Docstrings are mandatory** on every public module, class, and function.
  Google style, enforced by ruff `D` with `convention = "google"`. Include
  `Args:`, `Returns:`, and `Raises:` where they apply.
- **Type annotations on every signature**, arguments and return alike.
- **No `print`.** ruff `T20` rejects it. Library code returns values or logs.
- **Security lints are live.** ruff `S` (bandit) applies — no `assert` for
  runtime checks, no `subprocess` with `shell=True`, no hardcoded secrets.
- **Max cyclomatic complexity 15.** Past that, split the function.

## Conventions

- **No runtime dependencies ship with this template.** `dependencies` in
  `pyproject.toml` is empty on purpose — reach for the standard library first,
  and add a dependency with `uv add` only when it earns its place.
- Validate external data at the boundary. A dataclass with `__post_init__` is
  enough for simple cases; add pydantic when schemas get real.
- Raise with a message bound to a variable first (`msg = "..."; raise
  ValueError(msg)`) — ruff flags long literals inside `raise`.
- See `example.py` for the reference style. Delete it once real code exists.
