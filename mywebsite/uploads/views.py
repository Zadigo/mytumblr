import re
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.views.generic import FormView
from nltk.tokenize import TweetTokenizer

from notifications import choices as notification_choices
from notifications import models as notification_models
from tags import models
from uploads import forms

MYUSER = get_user_model()

def parse_text(tokens):
    instances = []
    for token in tokens:
        if token.startswith('#'):
            true_value = re.match(r'\#(\w+)', token)
            if true_value:
                value = true_value.group(1)
                if value is not None and value != '':
                    new_or_existing_value, _ = models.Tag.objects.get_or_create(title=value)
                    instances.append(new_or_existing_value)
    return instances


def parse_users(tokens):
    users_to_search = []
    for token in tokens:
        if token.startswith('@'):
            true_value = re.match(r'\@(\w+)', token)
            if true_value:
                value = true_value.group(1)
                if value is not None and value != '':
                    users_to_search.append(value)

    user_objects = MYUSER.objects.filter(username__in=users_to_search)
    return user_objects


class UploadView(LoginRequiredMixin, FormView):
    form_class = forms.UploadForm
    template_name = 'pages/new.html'
    success_url = '/feed/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            tokenizer = TweetTokenizer()

            new_video = form.save(commit=False)
            new_video.reference = secrets.token_hex(5)
            new_video.user = request.user
            new_video.views = 0
            
            new_video.save()

            tokens = tokenizer.tokenize(new_video.caption)
            new_tags = parse_text(tokens)

            new_video.tags.set(new_tags, clear=True)

            users = parse_users(tokens)
            if users.exists():
                notifications_to_create = [
                    notification_models.Notification(
                        user=user,
                        video=new_video,
                        notification_type=notification_choices.NotificationTypes.SHOUTOUT
                    )
                    for user in users
                ]
                notification_models.Notification.objects.bulk_create(notifications_to_create)
                
                # for item in notifications_to_create:
                #     item.save()
                    
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
