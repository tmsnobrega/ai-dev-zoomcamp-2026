# Homework 1: Household Chores

This Django application helps a single household assign chores and see what
needs attention. It intentionally has a small scope so the complete workflow is
easy to understand, test, and reproduce.

## Features

- Add and view household members.
- Create chores with an assignee and due date.
- Mark chores as completed.
- View outstanding, overdue, and completed chores on one dashboard.

Authentication, notifications, recurring chores, and multiple households are
outside this homework's scope.

## Run the application

1. Install the dependencies:

   ```powershell
   uv sync
   ```

2. Create the local database:

   ```powershell
   uv run python manage.py migrate
   ```

3. Start the development server:

   ```powershell
   uv run python manage.py runserver
   ```

4. Open `http://127.0.0.1:8000/`.

## Run the tests

```powershell
uv run python manage.py test
```

## Supporting documents

- [`_docs/plan.md`](_docs/plan.md): agreed product specification.
- [`_docs/backlog.md`](_docs/backlog.md): implementation tasks.
- [`_docs/homework-answers.md`](_docs/homework-answers.md): answers for submission.
- [`_docs/validation.md`](_docs/validation.md): checks performed before delivery.
