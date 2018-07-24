from django.contrib import admin
from .models import Issue, Comment

admin.site.register(Issue)
admin.site.register(Comment)