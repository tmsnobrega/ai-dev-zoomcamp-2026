# Mini Kanban board specification

## Purpose

Small teams need a simple way to see which tasks are planned, in progress, or done. This app keeps one shared board on a single device/server. It is deliberately smaller than a project-management service.

## Name

TaskLane

## Users and main flow

Anyone with the local app URL can see the board. A user adds a task with a short title and optional description, then moves it between To do, In progress, and Done. Another browser pointed at the same server sees the changes after refreshing. Tasks survive a server restart because they are stored in SQLite.

## Required behavior

1. List tasks grouped by status, ordered by creation time.
2. Create a task with a non-empty title of at most 100 characters and an optional description of at most 500 characters.
3. Move a task to any of the three statuses.
4. Delete a task only after the user confirms in the browser.
5. Show clear loading, empty, and error states.

## Data rules

- Each task has a server-generated unique ID, title, description, status, and creation timestamp.
- The server validates every write; the frontend validation is only for convenience.
- One SQLite database is the source of truth. The frontend never stores the task list as durable data.
- A missing task returns 404. Invalid input returns 422.

## Acceptance checks

- Creating a valid task returns it and displays it in To do.
- Moving it updates both the API and board after refresh.
- Deleting it removes it from the board and API.
- Two browser sessions show the same saved tasks after refresh.
- Invalid titles and unsupported statuses are rejected without changing the database.
- Tests run against an isolated temporary database.

## Out of scope

Accounts, permissions, attachments, due dates, drag-and-drop, live WebSocket sync, multiple boards, and deployment are not needed for Homework 2.
