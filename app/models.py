from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from mptt.fields import TreeForeignKey


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dislikes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    theme = models.CharField(max_length=50)
    sphere = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    create = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    likes = GenericRelation(Like)
    dislikes = GenericRelation(Dislike)

    def __str__(self):
        return f"id {self.id}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    create = models.DateTimeField(auto_now=True)

    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )


    def __str__(self):
        return f"{self.author} - {self.post}"


class Statistic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    total_posts_likes = models.PositiveIntegerField(default=0)
    total_posts_dislikes = models.PositiveIntegerField(default=0)

    total_comments = models.PositiveIntegerField(default=0)
    total_posts = models.PositiveIntegerField(default=0)

    total_self_posts_likes = models.PositiveIntegerField(default=0)
    total_self_posts_dislikes = models.PositiveIntegerField(default=0)
