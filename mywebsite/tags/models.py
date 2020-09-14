from django.db import models
from django.shortcuts import reverse
from tags import validators


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True, validators=[validators.title])
    created_on = models.DateField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tags:tag', args=[self.title])
