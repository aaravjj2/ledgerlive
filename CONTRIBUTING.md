# Contributing to LedgerLive

Thank you for your interest in contributing!

## Getting Started

```bash
git clone <repo-url> && cd ledgerlive
cp .env.example .env
make demo
```

## Development Setup

- **Python 3.12+** -- backend (FastAPI)
- **Node 22+** -- web frontend (Vite + React)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd apps/web && npm install && cd ../..
make dev        # starts API + web dev server
```

## Code Style

### Python
- **Formatter:** `black` (line length 100)
- **Import sorting:** `isort` (profile = black)
```bash
black apps/api && isort apps/api
```

### TypeScript
- **Linter:** `eslint` with project config
```bash
cd apps/web && npx eslint --fix .
```

Keep files under 800 lines. Prefer immutable data patterns.

## Running Tests

```bash
make test           # all Python tests
make e2e-mcp        # MCP end-to-end suite
pytest apps/api/tests/ -v                          # verbose
pytest apps/api/tests/ --cov=apps/api/app          # with coverage
```

Target: **80%+ line coverage** for new code.

## Pull Requests

1. Branch from `main`: `git checkout -b feat/my-feature main`
2. Make small, focused commits using **conventional commits**:

| Type       | When to use                      |
|------------|----------------------------------|
| `feat`     | New feature                      |
| `fix`      | Bug fix                          |
| `refactor` | Code change that is not feat/fix |
| `docs`     | Documentation only               |
| `test`     | Adding or updating tests         |
| `chore`    | Build, CI, tooling changes       |

3. Ensure tests pass and linting is clean.
4. Open a PR with a short title (< 70 chars), a Summary, and a Test Plan.
5. Address review feedback, then squash-merge when approved.

```
feat: add three-way match reconciliation endpoint
fix: correct FX rate lookup for intercompany eliminations
```
