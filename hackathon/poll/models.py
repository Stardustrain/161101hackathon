from django.db import models
from member.models import ServiceUser


class Poll(models.Model):
    title = models.CharField(max_length=200)
    notification = models.CharField(max_length=200,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(ServiceUser)


class Result(models.Model):
    student = models.ForeignKey(ServiceUser)
    score = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll)


class Comment(models.Model):
    student = models.ForeignKey(ServiceUser)
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=200)
    like = models.IntegerField(default=0)





