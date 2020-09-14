import json

from django import template
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model

from accounts import models as accounts_models
from tags import models

register = template.Library()

MYUSER = get_user_model()

@register.simple_tag
def users(request):
    current_user = MYUSER.objects.get(id=request.user.id)
    current_followers = current_user.myuserprofile.follows.all()
    list_of_ids = current_followers.values_list('id', flat=True)
    users = MYUSER.objects.exclude(id__in=list_of_ids)
    values = json.dumps(list(users.values('id', 'username')))
    return {'profiles': values}

@register.inclusion_tag('project_components/')
def tags():
    tags = models.Tag.objects.all()
    return {'tags': tags[:10]}
