from django.test import TestCase
from .models import Issue, Comment
from django.contrib.auth.models import User


class TestIssueModel(TestCase):


    def test_create_issue(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description", author=user, price=200, tag="TEST")
        issue.save()
        self.assertEqual(issue.title, "Test Issue Title")
        self.assertEqual(issue.description, "Test Issue Description")
        self.assertEqual(issue.author, user)
        self.assertIsNone(issue.assignee)
        self.assertIsNone(issue.resolved_date)
        self.assertEqual(issue.price, 200)
        self.assertEqual(issue.issue_type, "BUG")
        self.assertEqual(issue.status, "TODO")
        self.assertEqual(issue.tag, "TEST")
        self.assertEqual(issue.upvotes, 0)
        self.assertFalse(issue.is_resolved)

    def test_create_comment(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description", author=user, price=200)
        issue.save()
        comment = Comment(comment="Test Issue Comment", author=user, issue=issue)
        comment.save()
        self.assertEqual(comment.comment, "Test Issue Comment")
        self.assertEqual(comment.author, user)
        self.assertEqual(comment.issue, issue)


