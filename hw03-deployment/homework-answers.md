# Homework 3 answers

1. **Project architecture:** Agents claim tasks from a database through an
   HTTP API. The starter project's `SPEC.md` describes a shared relay that
   stores tasks and delivery attempts, while recipient agents claim work from
   the API.
2. **Status after the recipient submits its result:** `completed`. This is the
   exact terminal task state named by the starter `SPEC.md` after a recipient
   submits its result.
3. **Docker option to publish a container port to the host:** `-p` (or
   `--publish`).
4. **Postgres hostname from the API container in Docker Compose:** `postgres`,
   assuming the Compose service is named `postgres`.
5. **Kubernetes resource that keeps the requested replicas running and manages
   updates:** `Deployment`.
6. **If a test fails:** Keep the existing version running and stop the
   deployment. A failed check must block the release.

These answers correspond to the six questions on the course form. Each choice
is supported by the starter specification or the Docker, Compose, Kubernetes,
and CI behavior implemented in this folder.
