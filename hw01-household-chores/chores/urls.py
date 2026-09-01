"""Define the public routes for the chores application."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("members/", views.members, name="members"),
    path("chores/add/", views.add_chore, name="add_chore"),
    path("chores/<int:chore_id>/complete/", views.complete_chore, name="complete_chore"),
]
