from .models import Issue
import django_filters

class IssueFilter(django_filters.FilterSet):
    class Meta:
        model = Issue
        fields = ['issue_type', 'status', 'is_resolved', 'tag', 'author', 'assignee']