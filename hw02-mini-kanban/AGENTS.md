# TaskLane implementation rules

- Follow `_docs/specs.md` as the behavior contract.
- Keep API calls in `frontend/src/api.js`; no direct fetches in the board UI.
- Use a mock frontend API only for the prototype stage; the finished app uses FastAPI.
- Store tasks in SQLite through SQLAlchemy and keep tests isolated.
- Keep comments limited to steps whose purpose would otherwise be unclear.
- Run backend and frontend checks before committing work.

