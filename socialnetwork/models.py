from django.db import models
from django.contrib.auth.models import User

#Data model for a post
class Post(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()

    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + ',datetime=' + self.datetime + '"'

class Comment(models.Model):
    comment_text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()
    post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)

#Data model for a profile
class Profile(models.Model):
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    following = models.ManyToManyField(User, related_name="followers")

    def __str__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'






