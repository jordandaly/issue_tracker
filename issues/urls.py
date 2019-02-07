from django.conf.urls import url
from .views import get_issues, issue_detail, create_issue, edit_issue, create_or_edit_comment, search, get_issue_type_json, get_status_json, get_bug_upvotes_json, get_feature_upvotes_json, report, upvote, my_issues, my_notifications, create_or_edit_reply, save_issue, saved_issues, delete_saved_issue, do_search, do_search_my



urlpatterns = [
    url(r'^my_issues$', my_issues, name='my_issues'),
    url(r'^saved_issues', saved_issues, name='saved_issues'),
    url(r'^notifications$', my_notifications, name='my_notifications'),
    url(r'^$', get_issues, name='get_issues'),
    url(r'^(?P<pk>\d+)/$', issue_detail, name='issue_detail'),
    url(r'^new/$', create_issue, name='new_issue'),
    url(r'^(?P<pk>\d+)/edit/$', edit_issue, name='edit_issue'),
    url(r'^(?P<issue_pk>\d+)/new/$', create_or_edit_comment, name='new_comment'),
    url(r'^(?P<issue_pk>\d+)/(?P<pk>\d+)/edit/$', create_or_edit_comment, name='edit_comment'),
    url(r'^(?P<issue_pk>\d+)/(?P<comment_pk>\d+)/new/$', create_or_edit_reply, name='new_reply'),
    url(r'^(?P<issue_pk>\d+)/(?P<comment_pk>\d+)/(?P<pk>\d+)/edit/$', create_or_edit_reply, name='edit_reply'),
    url(r'^search/$', search, name='search'),
    url(r'^do_search/$', do_search, name='do_search'),
    url(r'^do_search_my/$', do_search_my, name='do_search_my'),
    url(r'^report/get_issue_type_json/$', get_issue_type_json, name='get_issue_type_json'),
    url(r'^report/get_status_json/$', get_status_json, name='get_status_json'),
    url(r'^report/get_bug_upvotes_json/$', get_bug_upvotes_json, name='get_bug_upvotes_json'),
    url(r'^report/get_feature_upvotes_json/$', get_feature_upvotes_json, name='get_feature_upvotes_json'),
    url(r'^report/$', report, name='report'),
    url(r'^(?P<pk>\d+)/upvote/$', upvote, name='upvote'),
    url(r'^(?P<pk>\d+)/save_issue/$', save_issue, name='save_issue'),
    url(r'^(?P<pk>\d+)/delete_saved_issue/$', delete_saved_issue, name='delete_saved_issue'),
    ]
