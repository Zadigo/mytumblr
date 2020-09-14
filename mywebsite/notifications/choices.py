from django.db import models


class NotificationTypes(models.Choices):
    MESSAGE = 'Message'
    FOLLOW = 'Follow'
    LIKE = 'Like'
    SHOUTOUT = 'Shoutout'
