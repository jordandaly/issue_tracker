from django.conf.urls import url
from .views import get_issues, issue_detail, create_or_edit_issue, create_or_edit_comment, search

urlpatterns = [
    url(r'^$', get_issues, name='get_issues'),
    url(r'^(?P<pk>\d+)/$', issue_detail, name='issue_detail'),
    url(r'^new/$', create_or_edit_issue, name='new_issue'),
    url(r'^(?P<pk>\d+)/edit/$', create_or_edit_issue, name='edit_issue'),
    url(r'^(?P<issue_pk>\d+)/new/$', create_or_edit_comment, name='new_comment'),
    url(r'^(?P<issue_pk>\d+)/(?P<pk>\d+)/edit/$', create_or_edit_comment, name='edit_comment'),
    url(r'^search/$', search, name='search'),
    ]
