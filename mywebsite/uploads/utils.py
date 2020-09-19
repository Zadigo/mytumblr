from django.apps import apps
from django.core import settings
from django.core.exceptions import ImproperlyConfigured

def get_feed_model():
    try:
        return apps.get_model(settings.FEED_MODEL)
    except:
        raise ImproperlyConfigured(
            'Please configure a model to use for uploading user items to'    
        )
