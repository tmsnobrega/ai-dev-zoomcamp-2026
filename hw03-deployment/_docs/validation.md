# Homework 3 validation record

Checked on 17 September 2026. Source of assignment scope: the [official
Homework 3 instructions](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/03-deployment/homework.md).
The six quiz answers and explanations are in [`../homework-answers.md`](../homework-answers.md).

## Assignment steps completed

- Read `SPEC.md` and the starter project. Confirmed the flow: sender creates a
  queued task, recipient claims it through the API, and sender can read the
  result after the status becomes `completed`.
- Ran the starter SQLite protocol suite before changes: 4 tests passed.
- Added PostgreSQL row-level locking for task claims (`FOR UPDATE SKIP LOCKED`)
  and consistent task/attempt locks for recovery and completion. Retained the
  SQLite test path.
- Re-ran the SQLite protocol suite: **4 passed** (one upstream Starlette/httpx
  deprecation warning).
- Built and ran the standalone production container with host port 18001
  published to container port 8000. Verified the dashboard said `Agent Relay
  v2`, and the sender saw a completed result. The temporary test container was
  stopped and removed.
- Built the Docker `test` image and ran the separate Compose PostgreSQL stack.
  The two-agent HTTP integration test raced two claims, completed the task, and
  verified the sender's result: **1 passed**.
- Built the production Docker image `agent-relay:hw03-local` and deployed it
  with PostgreSQL to a local `kind` cluster. Confirmed both pods ready, the
  PostgreSQL PVC bound, and the app Service available.
- Port-forwarded the live service. Verified `/ready` returned `ready`, the
  dashboard showed `Agent Relay v2`, and a live sender/recipient task flow
  ended as `completed` with the expected result.
- Added `.github/workflows/ci.yml`: tests run in one job; a dependent job builds
  the image and deploys to a disposable `kind` cluster only after tests pass.
- Ran the full workflow locally with `act`: the four SQLite tests passed, the
  PostgreSQL HTTP integration test passed, the unique image was loaded into
  `kind`, rollouts completed, and the smoke test confirmed both `/ready` and
  the `Agent Relay v2` dashboard heading.

## Quiz answers

1. Agents claim tasks from a database through an HTTP API.
2. `completed`.
3. `-p`.
4. `postgres`.
5. `Deployment`.
6. Keep the existing version running and stop deployment.

## Course form submission

- Submitted through the [Homework 3 course form](https://courses.datatalks.club/ai-dev-tools-2026/homework/hw3) on 17 September 2026.
- The form confirmed: “Thank you for submitting your homework, now your solution is saved.” Its status changed to `Submitted` and showed `Last saved at 17 September 2026 (Thu), 16:38` in the account timezone.
- Verified all six saved choices against `../homework-answers.md`; the public project URL points to `https://github.com/tmsnobrega/ai-dev-zoomcamp-2026/tree/main/hw03-deployment`.
- Optional lecture/homework hours, social links, and FAQ contribution were left blank because no accurate values or links were provided.

## Remaining external steps

- The official instructions also say to fork the upstream Agent Relay starter.
  The starter files are included here, but the connected GitHub tools do not
  expose a fork operation; no separate fork was created.
- Learning-in-public social posts are examples/requests to share. No post was
  created; the user should review and publish one personally if desired.

