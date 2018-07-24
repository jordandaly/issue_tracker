from django import forms
from .models import Issue, Comment


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'description', 'image', 'tag', 'issue_type')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)