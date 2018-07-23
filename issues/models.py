from django.db import models
from django.utils import timezone
from .utils import ChoiceEnum
from django.contrib.auth.models import User

class Issue(models.Model):
    """
    A single Issue
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_date = models.DateTimeField(blank=True, null=True)
    upvotes = models.IntegerField(default=0)
    tag = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='img', blank=True, null=True)
    author = models.ForeignKey(User,related_name='issue_author', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User,related_name='issue_assignee', null=True, on_delete=models.CASCADE)

    # Encapsulation, we meet again.
    class Issue_Types(ChoiceEnum):
        BUG = 'bug'
        FEATURE = 'feature'

    class Statuses(ChoiceEnum):
        TODO = 'todo'
        DOING = 'doing'
        DONE = 'done'

    issue_type = models.CharField(max_length=9, choices=Issue_Types.choices(), default='bug')
    status = models.CharField(max_length=7, choices=Statuses.choices(), default='todo')

    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
