from django.contrib import admin
from .models import Issue, Comment, Reply, SavedIssue

# Register your models here.


class CommentAdminInline(admin.StackedInline):
    model = Comment


class CommentAdmin(admin.ModelAdmin):
    inlines = (CommentAdminInline, )


class ReplyAdminInline(admin.StackedInline):
    model = Reply


class ReplyAdmin(admin.ModelAdmin):
    inlines = (ReplyAdminInline,)


admin.site.register(Issue, CommentAdmin)

admin.site.register(Comment, ReplyAdmin)

admin.site.register(SavedIssue)