# thelepath
Local RAG system for any sources

## Commit Tags

- `tidy` (Safe): Code cleanup, renaming, configs, docs, styles.
- `feat` (Creation): New behavior, new buttons, new features.
- `fix` (Repair): Fixing things that don't work as planned.

### Commit examples (best practices)

Template: `tag(place): what has been done`

- `tidy(docs): add project description to README`
- `tidy(domain): update code documentation in docstring`

## Backend

### Commands

`uv run ruff check . --fix && uv run ruff format . && uv run mypy .`

`uv run ruff check . --fix` — finds errors, removes unused imports, and fixes them.

`uv run ruff format .` — formats the code, standardizing quotes and empty lines. This is the command you were thinking of.

`uv run mypy .` — checks that you haven't passed a string instead of a number (static type checking).