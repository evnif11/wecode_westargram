from django.db import models
from django.db.models.deletion import CASCADE

from users.models import User

class Posting(models.Model):
    image_url       = models.CharField(max_length=1000)
    content         = models.CharField(max_length=1000, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    number_of_likes = models.IntegerField(default=0)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "postings"

class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=1000)

    class Meta:
        db_table = "comments"
