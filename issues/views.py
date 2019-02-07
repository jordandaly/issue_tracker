import os
import requests
from datetime import datetime, timedelta, time
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Count, Q
from django.core import serializers
from .models import Issue, Comment, Reply, SavedIssue
from .forms import IssueForm, CommentForm, ReplyForm
from .filters import IssueFilter
from notifications.signals import notify
from notifications.models import Notification



def report(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    completed_daily = Issue.objects.filter(resolved_date__gte=today_start).filter(resolved_date__lt=today_end).count()

    this_week_start = datetime.combine(today - timedelta(7), time())
    completed_weekly = Issue.objects.filter(resolved_date__gte=this_week_start).filter(resolved_date__lt=today_end).count()

    this_month_start = datetime.combine(today - timedelta(28), time())
    completed_monthly = Issue.objects.filter(resolved_date__gte=this_month_start).filter(resolved_date__lt=today_end).count()
    print(completed_daily)

    return render(request, "report.html", {'completed_daily': str(completed_daily), 'completed_weekly': str(completed_weekly), 'completed_monthly': str(completed_monthly)})


def get_issues(request):
    """
    Create a view that will return a list
    of Issues render them to the 'issues.html' template
    """
    
    issue_list = Issue.objects.all().order_by('-created_date')

    # Pagination settings
    page = request.GET.get('page', 1)
    paginator = Paginator(issue_list, 10)
    
    try:
        issues = paginator.page(page)
        
    except PageNotAnInteger:
        
        issues = paginator.page(1)
        
    except EmptyPage:
        
        issues = paginator.page(paginator.num_pages)

    return render(request, "issues.html", {'issues': issues})


def do_search(request):
    """
    Create a view for searching all issues by keyword search on Issue.Title to return a list
    of matching Issues and render them to the 'issues.html' template
    """
    issues = Issue.objects.filter(title__icontains=request.GET['q'])
    return render(request, "issues.html", {"issues": issues})

def do_search_my(request):
    """
    Create a view for searching my issues by keyword search on Issue.Title to return a list
    of matching Issues and render them to the 'myissues.html' template
    """
    user = request.user.id
    issues = Issue.objects.filter(author=user).filter(title__icontains=request.GET['q'])
    return render(request, "myissues.html", {"issues": issues})


@login_required()
def my_issues(request):
    """
    Create a view that will return a list
    of current user's Issues and render them to the 'myissues.html' template
    """
    user = request.user.id
    issues = Issue.objects.filter(author=user).order_by('-created_date')
    return render(request, "myissues.html", {'issues': issues})


@login_required()
def saved_issues(request):
    """
    Create a view that will return a list
    of current user's Saved Issues and render them to the 'issues.html' template
    """
    user = request.user.id
    savedissues = SavedIssue.objects.filter(user=user).order_by('-created_date')
    return render(request, "savedissues.html", {'savedissues': savedissues})


def my_notifications(request):
    """
    Create a view that will return a list
    of notifications for the user to the 'notifications.html' template
    """

    user = request.user.id
    notifications = Notification.objects.unread().filter(recipient=user).order_by('-timestamp')
    return render(request, "notifications.html", {'notifications': notifications})


def get_issue_type_json(request):
    dataset = Issue.objects \
        .values('issue_type') \
        .exclude(issue_type='') \
        .annotate(total=Count('issue_type')) \
        .order_by('issue_type')

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Issue Type'},
        'xAxis': {'type': "category"},
        'series': [{
            'name': 'Issue Type',
            'data': list(map(lambda row: {'name': [row['issue_type']], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)


def get_status_json(request):
    dataset = Issue.objects \
        .values('status') \
        .exclude(status='') \
        .annotate(total=Count('status')) \
        .order_by('status')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Issue Status'},
        'series': [{
            'name': 'Issue Status',
            'data': list(map(lambda row: {'name': [row['status']], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)

def get_bug_upvotes_json(request):
    dataset = Issue.objects \
        .filter(issue_type='BUG') \
        .values('upvotes', 'title') \
        .exclude(upvotes=0) \
        .order_by('upvotes')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Top Bug Upvotes'},
        'series': [{
            'name': 'Issue Upvotes',
            'data': list(map(lambda row: {'name': [row['title']], 'y': row['upvotes']}, dataset))
        }]
    }

    return JsonResponse(chart)

def get_feature_upvotes_json(request):
    dataset = Issue.objects \
    .filter(issue_type='FEATURE') \
    .values('upvotes', 'title') \
    .exclude(upvotes=0) \
    .order_by('upvotes')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Top Feature Upvotes'},
        'series': [{
            'name': 'Issue Upvotes',
            'data': list(map(lambda row: {'name': [row['title']], 'y': row['upvotes']}, dataset))
        }]
    }

    return JsonResponse(chart)


@login_required()
def search(request):
    issue_list = Issue.objects.all()
    issue_filter = IssueFilter(request.GET, queryset=issue_list)
    return render(request, 'search_issues.html', {'filter': issue_filter})


@login_required()
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
    comment_replies = []
    for comment in comments:
        replies = Reply.objects.filter(comment=comment)
        comment_replies.append(replies)

    return render(request, "issuedetail.html", {'issue': issue, 'comments': comments, 'comment_replies': comment_replies})


@login_required()
def upvote(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.upvotes += 1
    issue.save()
    notify.send(request.user, recipient=issue.author, verb="upvoted your Issue: " + issue.title)
    messages.success(request, 'Issue upvoted!')
    return redirect('issue_detail', pk)

@login_required()
def save_issue(request, pk):
    user = request.user
    issue = Issue.objects.get(pk=pk)
    try:
        savedissue = SavedIssue.objects.get(user=user, issue=issue)
    except SavedIssue.DoesNotExist:
        savedissue = None
    if savedissue is None:
        savedissue = SavedIssue(user=user, issue=issue)
        savedissue.save()
        messages.success(request, 'Issue added to your Saved Issues!')
    else:
        messages.error(request, 'Issue already added in your Saved Issues!')
    return redirect('issue_detail', pk)

@login_required()
def delete_saved_issue(request, pk):
    savedissue = SavedIssue.objects.get(pk=pk)
    savedissue.delete()
    messages.success(request, 'Saved Issue deleted!')
    return redirect('saved_issues')


@login_required()
def create_issue(request):
    """
    Create a view that allows us to create an issue depending if the Issue ID
    is null or not
    """
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.instance.author = request.user
            if form.instance.issue_type == 'FEATURE':
                form.instance.price = 100
            else:
                form.instance.price = 0
            issue = form.save()
            
            return redirect(issue_detail, issue.pk)
    else:
        form = IssueForm()
    return render(request, 'issueform.html', {'form': form})


@login_required()
def edit_issue(request, pk=None):
    """
    Create a view that allows us to edit a issue depending if the Issue ID
    is null or not
    """
    issue = get_object_or_404(Issue, pk=pk) if pk else None
    user = request.user
    # Prevents a non-staff user from editing another users comment
    if not request.user.is_staff:
        if user.id != request.user.id:
            messages.success(
                request,
                'You Do Not Have Permission To Edit this Issue'
            )
            return redirect(issue_detail, issue.pk)

    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():

            form.instance.author = request.user
            if form.instance.issue_type == 'FEATURE':
                form.instance.price = 100
            else:
                form.instance.price = 0
            issue = form.save()
            notify.send(request.user, recipient=issue.author, verb="updated your Issue: " + issue.title)
            messages.success(request, 'Issue Edited with success!')

            return redirect(issue_detail, issue.pk)
    else:
        form = IssueForm(instance=issue)
    return render(request, 'issueform.html', {'form': form})


@login_required()
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
            form.save()
            notify.send(request.user, recipient=issue.author, verb="added a comment to your Issue: " + issue.title)
            messages.success(request, 'Comment Saved!')
            return redirect(issue_detail, issue_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'commentform.html', {'form': form})


@login_required()
def create_or_edit_reply(request, issue_pk, comment_pk, pk=None):
    """
    Create a view that allows us to create
    or edit a reply depending if the Reply ID
    is null or not
    """
    comment = get_object_or_404(Comment, pk=comment_pk)
    reply = get_object_or_404(Reply, pk=pk) if pk else None
    if request.method == "POST":
        form = ReplyForm(request.POST, request.FILES, instance=reply)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.comment = comment
            form.save()
            notify.send(request.user, recipient=comment.author, verb="added a reply to your Comment: " + comment.comment)
            messages.success(request, 'Reply Saved!')
            return redirect(issue_detail, issue_pk)
    else:
        form = ReplyForm(instance=reply)
    return render(request, 'replyform.html', {'form': form})



