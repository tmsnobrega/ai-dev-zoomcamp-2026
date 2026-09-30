# Homework 04: DevOps and observability

I added observability and an automatic incident responder to the course's
Order Tracker starter. The express-order lookup failed at month-end while the
app's health check still passed. The saved evidence records how Grafana detected
the failure, Codex proposed a fix, and the responder checked and deployed it.

- [My answers](order-tracker/docs/homework-answers.md)
- [App setup and commands](order-tracker/README.md)
- [Incident report](order-tracker/docs/incident-report.md)
- [Validation record](order-tracker/docs/validation.md)
- [Final check results](order-tracker/docs/evidence/final-validation.json)

The working starter fork is [tmsnobrega/order-tracker](https://github.com/tmsnobrega/order-tracker).
This course folder contains the same homework files as ordinary files, not a
Git submodule.
