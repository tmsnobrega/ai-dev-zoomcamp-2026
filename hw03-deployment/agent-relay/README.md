# Agent Relay v2 — Homework 03

Agent Relay lets two agents exchange a task through an HTTP API. The sender
creates a task; the recipient claims it, processes it, and returns a result.
The service stores task state in PostgreSQL and the included example worker
deterministically returns `input.upper()`.

## Run with Docker Compose

```bash
docker compose up --build
```

Open <http://127.0.0.1:8000/> for the dashboard. Compose waits for PostgreSQL
readiness before starting the API and keeps database files in the `relay-data`
volume. `/health` checks the API process; `/ready` also checks the real database
tables. Local credentials in `compose.yaml` are examples only. Set strong
values in a local `.env` file and never use these defaults on a public server.

Register two identities and send a task:

```bash
alice=$(curl -sS -X POST http://127.0.0.1:8000/api/v1/agents \
  -H 'content-type: application/json' -d '{"name":"alice"}')
bob=$(curl -sS -X POST http://127.0.0.1:8000/api/v1/agents \
  -H 'content-type: application/json' -d '{"name":"uppercase"}')
```

Each response includes a secret token once. Keep it outside source control.
Use `Authorization: Bearer <agent-token>` for later calls. For a shared local
installation, set `RELAY_ENROLLMENT_SECRET` and provide it as
`X-Enrollment-Secret` when registering.

## Storage and delivery behavior

`database.py` owns SQLAlchemy models and transaction boundaries; `storage.py`
owns task operations. SQLite tests use a serialized writer transaction.
PostgreSQL claims lock a queued task with `FOR UPDATE SKIP LOCKED`, so parallel
API processes cannot claim the same work. Expiry recovery and completion lock
the task first and its attempt second. The HTTP protocol remains in `SPEC.md`.
Claims are at-least-once and leased. Heartbeats extend an active lease, while a
stale claim token cannot complete a task.

## Tests

The starter protocol suite covers the API, permissions, expiry, and concurrent
claims. It uses a scratch SQLite database; its fixture recreates all tables in
the configured database, so do not point it at data you need.

```bash
uv sync --frozen
uv run pytest -q test_agent_relay.py
```

The HTTP integration test uses two agents, races two claim requests against a
disposable PostgreSQL service, completes the task, and verifies the sender's
result:

```bash
docker compose --profile test up --build --abort-on-container-exit --exit-code-from integration integration
docker compose --profile test down
```

The test profile uses an ephemeral database container. `down` removes the test
containers without removing the named `relay-data` development volume.

## Docker image

```bash
docker build -t agent-relay:local .
docker run --rm -p 8000:8000 -e RELAY_DATABASE_URL='postgresql+psycopg://relay:password@host.docker.internal:5432/relay' agent-relay:local
```

The `-p 8000:8000` option maps host port 8000 to the container's port 8000.
Provide reachable PostgreSQL credentials through environment variables.

## Kubernetes and CI

See [`docs/deployment.md`](docs/deployment.md) for a local `kind` deployment,
persistent database storage, locally created secrets, readiness checks, and
port-forwarding. `.github/workflows/ci.yml` runs tests first; its dependent job
builds and deploys to a throwaway `kind` cluster only if tests pass, then
smoke-tests `/ready`. See [`docs/testing.md`](docs/testing.md) for validation
commands and local `act` use.
