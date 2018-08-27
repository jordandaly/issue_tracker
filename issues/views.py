from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from .models import Issue, Comment
from .forms import IssueForm, CommentForm
from .filters import IssueFilter
from django.http import JsonResponse
from django.db.models import Count
from django.core import serializers
import os
import requests
from datetime import datetime, timedelta, time


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
    
    issues = Issue.objects.all().order_by('-created_date')
    return render(request, "issues.html", {'issues': issues})


@login_required()
def my_issues(request):
    """
    Create a view that will return a list
    of current user's Issues and render them to the 'issues.html' template
    """
    user = request.user.id
    issues = Issue.objects.filter(author=user).order_by('-created_date')
    return render(request, "issues.html", {'issues': issues})


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


def get_upvotes_json(request):
    dataset = Issue.objects \
        .values('upvotes', 'title') \
        .order_by('upvotes')

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': 'Issue Upvotes'},
        'yAxis': {'type': "category"},
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
    return render(request, "issuedetail.html", {'issue': issue, 'comments': comments})


@login_required()
def upvote(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.upvotes += 1
    issue.save()
    return redirect('issue_detail', pk)


@login_required()
def create_issue(request):
    """
    Create a view that allows us to create an issue depending if the Issue ID
    is null or not
    """
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
        
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.instance.author = request.user
                if form.instance.issue_type == 'FEATURE':
                    form.instance.price = 100
                else:
                    form.instance.price = 0
                issue = form.save()
                messages.success(request, 'New Issue added with success!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            
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
            comment = form.save()
            return redirect(issue_detail, issue_pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'commentform.html', {'form': form})


