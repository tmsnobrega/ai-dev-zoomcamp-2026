# TaskLane

TaskLane is a small Kanban board for one team. Add a task, move it between **To do**, **In progress**, and **Done**, or delete it. The FastAPI server saves tasks in SQLite, so refreshing the page or restarting the server does not erase them. This is a local development project, not a hosted service.

The [specification](_docs/specs.md) defines the scope and acceptance checks.

## Run it

You need Python 3.11+, [uv](https://docs.astral.sh/uv/), and Node.js 20+.

In one terminal:

```powershell
cd hw02-mini-kanban/backend
uv sync
uv run uvicorn app.main:app --reload
```

In another terminal:

```powershell
cd hw02-mini-kanban/frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. The frontend calls `http://127.0.0.1:8000/api/tasks`. The API docs are at `http://127.0.0.1:8000/docs`.

To run the frontend-only prototype, set `VITE_USE_MOCK=true` before `npm run dev`. Prototype tasks exist only in the browser session; the normal mode uses the persistent backend.

## Check it

```powershell
cd hw02-mini-kanban/backend
uv run pytest -q
cd ../frontend
npm run build
```

The backend tests cover create, list, move, delete, persistence after restarting the app, bad input, and missing tasks. They use a temporary SQLite database; they do not touch local board data.

## Project files

- `_docs/specs.md`: behavior, data rules, and boundaries.
- `frontend/src/api.js`: all frontend API calls and the in-memory prototype.
- `frontend/src/main.js`: the interactive board.
- `backend/app/main.py`: API and SQLite model.
- `backend/tests/test_tasks.py`: isolated API checks.
- `homework-answers.md`: concise responses for the course form.

No accounts, multiple boards, drag-and-drop, or deployment are included. Do not use this app for sensitive data: anyone who can reach this local server can change its tasks.
