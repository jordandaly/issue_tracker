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

def report(request):
    return render(request, "report.html")

def get_issues(request):
    """
    Create a view that will return a list
    of Issues render them to the 'issues.html' template
    """
    
    issues = Issue.objects.all().order_by('-created_date')
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

@login_required()
def upvote(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.upvotes += 1
    issue.save()
    return redirect('issue_detail', pk)

@login_required()
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


