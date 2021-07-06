import os
import secrets

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.expressions import F
from django.db.models.signals import post_delete
from django.dispatch import receiver
from tags import models as tags_models

from feed import logic, managers, validators
from feed.choices import MediaTypes

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

MYUSER = get_user_model()

class Music(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['name', 'artist'])
        ]

    def __str__(self):
        return self.name


class Video(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    user       = models.ForeignKey(MYUSER, on_delete=models.DO_NOTHING)
    caption  = models.CharField(max_length=100, blank=True, null=True)
    url   = models.FileField(upload_to=logic.upload_video_path, validators=[validators.file_type])
    thumbnail = ImageSpecField(
        source='url',
        processors=ResizeToFit(width=500),
        format='JPEG', 
        options={'quality': 50}
    )
    views       = models.PositiveIntegerField()

    # music = models.ForeignKey(Music, on_delete=models.SET_NULL, blank=True, null=True)
    media_type = models.CharField(max_length=50, choices=MediaTypes.choices, default=MediaTypes.IMAGE)

    reports   = models.IntegerField(default=0)
    reported     = models.BooleanField(default=False)
    visible   = models.BooleanField(default=True, help_text='For admin purposes')

    public = models.BooleanField(default=True)
    only_friends = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=True)
    can_duet_react = models.BooleanField(default=True)

    tags = models.ManyToManyField(tags_models.Tag, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on', '-pk']
        indexes = [
            models.Index(fields=['user', 'url'])
        ]

    objects = models.Manager()
    video_manager = managers.VideosManager.as_manager()

    def __str__(self):
        return self.reference
        
    def clean(self):
        if self.reference is None:
            self.reference = secrets.token_hex(5)
    
    def add_view(self):
        self.views = F('views') + 1
        return self.views


class Comment(models.Model):
    user    = models.ForeignKey(MYUSER, on_delete=models.CASCADE)
    video   = models.ForeignKey(Video, on_delete=models.CASCADE)
    text    = models.CharField(max_length=300)
    in_reply_to = models.IntegerField(blank=True, null=True)
    created_on  = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user        = models.ForeignKey(MYUSER, on_delete=models.CASCADE)
    video       = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True)
    comment   = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Search(models.Model):
    user = models.ForeignKey(MYUSER, on_delete=models.CASCADE, blank=True, null=True)
    term = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Searches'
        indexes = [
            models.Index(fields=['term'])
        ]

    def __str__(self):
        return self.user.username


@receiver(post_delete, sender=Video)
def delete_video(sender, instance, **kwargs):
    if instance.url:
        if os.path.isfile(instance.url.path):
            os.remove(instance.url.path)
