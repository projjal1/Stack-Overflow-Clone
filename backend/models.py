from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    tag = models.CharField(max_length=50)
    answers = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    views=models.IntegerField(default=0)

class Fixes(models.Model):
    question_id=models.IntegerField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=50)
    upvotes=models.IntegerField(default=0)
    abuse=models.BooleanField(default=False)