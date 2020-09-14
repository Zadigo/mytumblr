import secrets

from django import forms
from django.forms import widgets

from feed import models
from uploads import widgets as custom_widgets


class UploadForm(forms.ModelForm):
    class Meta:
        model = models.Video
        fields = ['caption', 'url', 'public', 'only_friends', 'can_comment', 'can_duet_react']
        labels = {
            'can_comment': 'Everyone can comment'
        }
        widgets = {
            'caption': custom_widgets.CustomTextInput(),
            'url': widgets.FileInput(),
            'public': custom_widgets.CustomCheckBoxInput(),
            'only_friends': custom_widgets.CustomCheckBoxInput(),
            'can_comment': custom_widgets.CustomCheckBoxInput(),
            'can_duet_react': custom_widgets.CustomCheckBoxInput(),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        new_file = cleaned_data['url']
        _, ext = new_file.name.split('.')
        new_file_name = secrets.token_hex(5)
        new_file.name = f'{new_file_name}.{ext}'
        return cleaned_data
