from django.test import TestCase
from django.contrib.auth.models import User
from .models import Issue, Comment

class LoggedInTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='Customer1', password='Pass1234')
        self.client.login(username='Customer1', password='Pass1234')


class TestViews(LoggedInTestCase):

    def test_get_issues_page(self):
        page = self.client.get("/issues/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "issues.html")

    def test_get_search_issues_page(self):
        page = self.client.get("/issues/search/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "search_issues.html")


    def test_get_add_issue_page(self):
        page = self.client.get("/issues/new/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "issueform.html")

    def test_get_edit_issue_page(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description", author=user, price=100)
        issue.save()

        page = self.client.get("/issues/{0}/edit/".format(issue.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "issueform.html")

    def test_get_issue_detail_page(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description", author=user, price=100)
        issue.save()

        page = self.client.get("/issues/{0}/".format(issue.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "issuedetail.html")

    def test_get_edit_issue_page_for_item_that_does_not_exist(self):
        page = self.client.get("/issues/1/edit/")
        self.assertEqual(page.status_code, 404)

    def test_get_issue_detail_page_for_item_that_does_not_exist(self):
        page = self.client.get("/issues/1/")
        self.assertEqual(page.status_code, 404)


    def test_get_add_comment_page(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description", author=user, price=100)
        issue.save()
        page = self.client.get("/issues/{0}/new/".format(issue.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "commentform.html")

    def test_get_edit_comment_page(self):
        user = User()
        user.save()
        issue = Issue(title="Test Issue Title", description="Test Issue Description", author=user, price=100)
        issue.save()
        comment = Comment(comment="Test Issue Comment", author=user, issue=issue)
        comment.save()

        page = self.client.get("/issues/{0}/{1}/edit/".format(issue.id, comment.id))
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "commentform.html")


    def test_get_edit_comment_page_for_item_that_does_not_exist(self):
        page = self.client.get("/issues/1/1/edit/")
        self.assertEqual(page.status_code, 404)

