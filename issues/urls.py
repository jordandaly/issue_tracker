from django.conf.urls import url
from .views import get_issues, issue_detail, create_issue, edit_issue, create_or_edit_comment, search, get_issue_type_json, get_status_json, get_upvotes_json, report, upvote, my_issues, my_notifications


urlpatterns = [
    url(r'^my_issues$', my_issues, name='my_issues'),
    url(r'^notifications$', my_notifications, name='my_notifications'),
    url(r'^$', get_issues, name='get_issues'),
    url(r'^(?P<pk>\d+)/$', issue_detail, name='issue_detail'),
    url(r'^new/$', create_issue, name='new_issue'),
    url(r'^(?P<pk>\d+)/edit/$', edit_issue, name='edit_issue'),
    url(r'^(?P<issue_pk>\d+)/new/$', create_or_edit_comment, name='new_comment'),
    url(r'^(?P<issue_pk>\d+)/(?P<pk>\d+)/edit/$', create_or_edit_comment, name='edit_comment'),
    url(r'^search/$', search, name='search'),
    url(r'^report/get_issue_type_json/$', get_issue_type_json, name='get_issue_type_json'),
    url(r'^report/get_status_json/$', get_status_json, name='get_status_json'),
    url(r'^report/get_upvotes_json/$', get_upvotes_json, name='get_upvotes_json'),
    url(r'^report/$', report, name='report'),
    url(r'^(?P<pk>\d+)/upvote/$', upvote, name='upvote'),
    ]
