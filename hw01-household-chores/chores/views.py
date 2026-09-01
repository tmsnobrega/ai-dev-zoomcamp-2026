"""Handle the dashboard, data-entry forms, and completion action."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ChoreForm, MemberForm
from .models import Chore, Member


def dashboard(request):
    today = timezone.localdate()
    context = {
        "outstanding_chores": Chore.objects.filter(
            completed_at__isnull=True, due_date__gte=today
        ),
        "overdue_chores": Chore.objects.filter(
            completed_at__isnull=True, due_date__lt=today
        ),
        "completed_chores": Chore.objects.filter(
            completed_at__isnull=False
        ).order_by("-completed_at"),
    }
    return render(request, "chores/dashboard.html", context)


def members(request):
    form = MemberForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Household member added.")
        return redirect("members")
    return render(
        request,
        "chores/members.html",
        {"form": form, "members": Member.objects.all()},
    )


def add_chore(request):
    form = ChoreForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Chore added.")
        return redirect("dashboard")
    return render(request, "chores/add_chore.html", {"form": form})


@require_POST
def complete_chore(request, chore_id):
    chore = get_object_or_404(Chore, id=chore_id)
    chore.complete()
    messages.success(request, "Chore marked as completed.")
    return redirect("dashboard")
