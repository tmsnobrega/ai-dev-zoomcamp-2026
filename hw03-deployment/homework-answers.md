# Homework 3 answers

1. **Project architecture:** Agents claim tasks from a database through an
   HTTP API. This is a pull-based task queue: the API and database hold the
   shared task state.
2. **Status after the recipient submits its result:** `completed`. The task
   work is finished; `delivered` describes message/result transport rather
   than the task's completion state.
3. **Docker option to publish a container port to the host:** `-p` (or
   `--publish`).
4. **Postgres hostname from the API container in Docker Compose:** `postgres`,
   assuming the Compose service is named `postgres`.
5. **Kubernetes resource that keeps the requested replicas running and manages
   updates:** `Deployment`.
6. **If a test fails:** Keep the existing version running and stop the
   deployment. A failed check must block the release.

These answers correspond to the six multiple-choice questions shown in the
course preview. The course form has not yet been submitted.

