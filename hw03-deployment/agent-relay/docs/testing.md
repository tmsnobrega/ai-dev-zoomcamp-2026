# Testing and local CI

## Unit tests

The protocol suite uses a scratch SQLite database and covers API behavior,
expiry, and concurrent claims:

```bash
uv sync --frozen
uv run pytest -q test_agent_relay.py
```

## PostgreSQL HTTP integration test

The Compose test profile starts an isolated PostgreSQL database and API. The
integration test registers two agents via HTTP, creates a task, races two
claim requests, completes it, and verifies the sender sees the result:

```bash
docker compose --profile test up --build --abort-on-container-exit --exit-code-from integration integration
docker compose --profile test down
```

The integration database is disposable and separate from the named
`relay-data` development volume. `down` removes its container without deleting
the named development volume.

## Run GitHub Actions locally with `act`

Install Docker Desktop and `act`. On Windows, make Git Bash, `kind`, and
`kubectl` available on `PATH`, then from this folder run:

```powershell
$env:PATH = "C:\Program Files\Git\bin;$env:LOCALAPPDATA\Microsoft\WinGet\Links;$env:PATH"
act -W .github/workflows/ci.yml -P ubuntu-latest=-self-hosted
```

The test job runs the four SQLite tests and the PostgreSQL HTTP integration
test. The dependent deploy job builds a unique image, loads it into kind,
applies PostgreSQL and Agent Relay, waits for rollouts, and checks `/ready` and
the `Agent Relay v2` dashboard heading.
For a local `act` run, first create and select a kind cluster; the workflow
reuses it instead of creating a nested cluster. GitHub Actions creates a fresh
cluster automatically. Local emulation differs from GitHub runners, so a
successful GitHub Actions run is additional evidence.
