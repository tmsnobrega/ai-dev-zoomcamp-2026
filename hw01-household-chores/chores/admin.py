"""Make homework data inspectable through Django's admin area."""

from django.contrib import admin

from .models import Chore, Member

admin.site.register(Member)
admin.site.register(Chore)
