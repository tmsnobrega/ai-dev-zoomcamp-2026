# Product Plan

## Problem

People who share a home can lose track of who is responsible for a chore and
when it is due. The application provides one clear place to record assignments
and completion.

## Users

The users are members of one shared household. This first version does not use
accounts or passwords.

## Features

1. **Manage members:** add a household member and view existing members.
2. **Assign chores:** create a chore with a title, optional description,
   assignee, and due date.
3. **Track completion:** mark an outstanding chore as completed and record the
   completion time.
4. **View status:** show outstanding, overdue, and completed chores in separate
   dashboard sections.

## Main workflow

1. Add the people who share the household.
2. Create a chore and assign it to one person.
3. Review the dashboard to see current and overdue work.
4. Mark the chore as completed when the work is finished.

## Rules

- A member's name is required and must be unique.
- A chore requires a title, an assignee, and a due date.
- Only incomplete chores can be marked as completed.
- A chore is overdue when it is incomplete and its due date is before today.

## Out of scope

- Authentication and user accounts.
- Email or mobile notifications.
- Recurring chores.
- Multiple households.
- Editing or deleting records.

## Acceptance criteria

- A visitor can add a member using a simple form.
- A visitor can create a valid chore for an existing member.
- The dashboard separates current, overdue, and completed chores correctly.
- Completing a chore moves it to the completed section.
- Invalid form submissions show clear validation messages.
- Automated tests cover the main workflows and status rules.
