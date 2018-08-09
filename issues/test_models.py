from django.test import TestCase
from .models import Issue, Comment
from django.contrib.auth.models import User


class TestIssueModel(TestCase):

    def test_defaults_issue_type_bug_status_todo_upvotes_0_isResolved_False(self):
        user = User()
        user.save()
        issue = Issue(author=user, price=100)
        issue.save()
        self.assertEqual(issue.issue_type, "bug")
        self.assertEqual(issue.status, "todo")
        self.assertEqual(issue.upvotes, 0)
        self.assertFalse(issue.is_resolved)

    def test_can_create_an_issue_with_a_title_and_description(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description",author=user, price=100)
        issue.save()
        self.assertEqual(issue.title, "Test Issue Title")
        self.assertEqual(issue.description, "Test Issue Description")
