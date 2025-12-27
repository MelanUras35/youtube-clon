from django.db import models
from django.contrib.auth.models import User
import uuid


def video_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'videos/{uuid.uuid4()}.{ext}'


def thumbnail_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'thumbnails/{uuid.uuid4()}.{ext}'


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to=video_upload_path)
    thumbnail = models.ImageField(upload_to=thumbnail_upload_path, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.video.title}'

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=True)  # True = like, False = dislike
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    channel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'channel')

    def __str__(self):
        return f'{self.subscriber.username} -> {self.channel.username}'
