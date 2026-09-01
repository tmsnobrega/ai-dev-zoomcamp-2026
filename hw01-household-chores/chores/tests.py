"""Verify the status rules and the complete browser workflow."""

from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chore, Member


class ChoreModelTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Alex")

    def test_incomplete_past_chore_is_overdue(self):
        chore = Chore.objects.create(
            title="Take out recycling",
            assignee=self.member,
            due_date=timezone.localdate() - timedelta(days=1),
        )

        self.assertTrue(chore.is_overdue)
        self.assertFalse(chore.is_completed)

    def test_completed_past_chore_is_not_overdue(self):
        chore = Chore.objects.create(
            title="Clean kitchen",
            assignee=self.member,
            due_date=timezone.localdate() - timedelta(days=1),
        )

        chore.complete()

        self.assertTrue(chore.is_completed)
        self.assertFalse(chore.is_overdue)


class HouseholdWorkflowTests(TestCase):
    def test_member_chore_and_completion_workflow(self):
        member_response = self.client.post(reverse("members"), {"name": "Sam"})
        member = Member.objects.get(name="Sam")

        chore_response = self.client.post(
            reverse("add_chore"),
            {
                "title": "Wash dishes",
                "description": "After dinner",
                "assignee": member.id,
                "due_date": timezone.localdate(),
            },
        )
        chore = Chore.objects.get(title="Wash dishes")
        dashboard_response = self.client.get(reverse("dashboard"))
        complete_response = self.client.post(reverse("complete_chore", args=[chore.id]))

        self.assertRedirects(member_response, reverse("members"))
        self.assertRedirects(chore_response, reverse("dashboard"))
        self.assertContains(dashboard_response, "Wash dishes")
        self.assertRedirects(complete_response, reverse("dashboard"))
        chore.refresh_from_db()
        self.assertTrue(chore.is_completed)

    def test_duplicate_member_name_shows_validation_error(self):
        Member.objects.create(name="Sam")

        response = self.client.post(reverse("members"), {"name": "Sam"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")
        self.assertEqual(Member.objects.count(), 1)

    def test_completion_requires_post(self):
        member = Member.objects.create(name="Sam")
        chore = Chore.objects.create(
            title="Vacuum",
            assignee=member,
            due_date=timezone.localdate(),
        )

        response = self.client.get(reverse("complete_chore", args=[chore.id]))

        self.assertEqual(response.status_code, 405)
        chore.refresh_from_db()
        self.assertFalse(chore.is_completed)
