"""Store household members and their assigned chores."""

from django.db import models
from django.utils import timezone


class Member(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Chore(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="chores")
    due_date = models.DateField()
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date", "title"]

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        return self.completed_at is not None

    @property
    def is_overdue(self):
        return not self.is_completed and self.due_date < timezone.localdate()

    def complete(self):
        """Record completion once and leave an existing timestamp unchanged."""
        if not self.is_completed:
            self.completed_at = timezone.now()
            self.save(update_fields=["completed_at"])
