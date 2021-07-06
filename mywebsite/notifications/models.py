from django.contrib.auth import get_user_model
from django.db import models

from feed import models as feed_models
from notifications.choices import NotificationTypes

MYUSER = get_user_model()

class Notification(models.Model):
    user    = models.ForeignKey(MYUSER, on_delete=models.CASCADE)
    video  = models.ForeignKey(feed_models.Video, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(feed_models.Comment, on_delete=models.CASCADE, blank=True, null=True)
    notification_type = models.CharField(max_length=50, choices=NotificationTypes.choices, default=NotificationTypes.FOLLOW)
    read        = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.user.username
