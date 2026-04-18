# thelepath
Local RAG system for any sources

## Backend

### Commands

`uv run ruff check . --fix && uv run ruff format . && uv run mypy .`

`uv run ruff check . --fix` — finds errors, removes unused imports, and fixes them.

`uv run ruff format .` — formats the code, standardizing quotes and empty lines. This is the command you were thinking of.

`uv run mypy .` — checks that you haven't passed a string instead of a number (static type checking).