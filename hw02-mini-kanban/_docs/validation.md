# Validation record

Checked on 12 September 2026 using Python 3.13, uv 0.9.9, and Node.js 25.

- `uv run pytest -q` in `backend`: 2 passed. Two third-party deprecation warnings were shown; no test failed.
- `npm install --cache .npm-cache` in `frontend`: installed dependencies; audit reported zero vulnerabilities.
- `npm run build` in `frontend`: production build passed.

The API tests use temporary SQLite files and check create, list, move, delete, persistence across app instances, invalid input, and 404 responses. Browser behavior has not been manually tested in this record. The optional video has not been recorded.

