from django import template
from django.shortcuts import reverse

register = template.Library()


@register.simple_tag
def follow_url(username):
    return reverse('feed:follow', args=[username])


@register.simple_tag
def unfollow_url(username):
    return reverse('feed:unfollow', args=[username])
