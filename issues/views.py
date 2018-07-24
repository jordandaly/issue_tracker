from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Issue, Comment
from .forms import IssueForm, CommentForm
from .filters import IssueFilter
from django.http import JsonResponse
from django.core import serializers

def report(request):
    return render(request, "report.html")


def get_issues(request):
    """
    Create a view that will return a list
    of Issues render them to the 'issues.html' template
    """
    
    issues = Issue.objects.all().order_by('-created_date')
    return render(request, "issues.html", {'issues': issues})


def get_issues_json(request):
    issues = []
    for i in Issue.objects.all():
        issues.append({
            'title': i.title,
            'description': i.description,
            'tag': i.tag,
            'resolved_date': i.resolved_date,
            'issue_type': i.issue_type,
            'status': i.status,
            'upvotes': i.upvotes,
            'author': i.author.username,
            'assignee': i.assignee.username
        })
    return JsonResponse(issues, safe=False)

def search(request):
    issue_list = Issue.objects.all()
    issue_filter = IssueFilter(request.GET, queryset=issue_list)
    return render(request, 'search_issues.html', {'filter': issue_filter})

def issue_detail(request, pk):
    """
    Create a view that returns a single
    Issue object based on the issue ID (pk) and
    render it to the 'issuedetail.html' template.
    Or return a 404 error if the issue is
    not found
    """
    issue = get_object_or_404(Issue, pk=pk)
    issue.save()
    comments = Comment.objects.filter(issue=pk)
    return render(request, "issuedetail.html", {'issue': issue, 'comments': comments})

def create_or_edit_issue(request, pk=None):
    """
    Create a view that allows us to create
    or edit a issue depending if the Issue ID
    is null or not
    """
    issue = get_object_or_404(Issue, pk=pk) if pk else None
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            form.instance.author = request.user
            issue = form.save()
            return redirect(issue_detail, issue.pk)
    else:
        form = IssueForm(instance=issue)
    return render(request, 'issueform.html', {'form': form})


def create_or_edit_comment(request, issue_pk, pk=None):
    """
    Create a view that allows us to create
    or edit a comment depending if the Comment ID
    is null or not
    """
    issue = get_object_or_404(Issue, pk=issue_pk)
    comment = get_object_or_404(Comment, pk=pk) if pk else None
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.issue = issue
            comment = form.save()
            return redirect(issue_detail, issue_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'commentform.html', {'form': form})


