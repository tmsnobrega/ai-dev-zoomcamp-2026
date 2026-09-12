# TaskLane implementation rules

- Follow `_docs/specs.md` and `openapi.yaml` as the behavior contract.
- Keep API calls in `frontend/src/api.ts`; no direct fetches in components.
- Use a mock frontend API only for the prototype stage; the finished app uses FastAPI.
- Store tasks in SQLite through SQLAlchemy and keep tests isolated.
- Keep comments limited to steps whose purpose would otherwise be unclear.
- Run backend and frontend checks before committing work.
