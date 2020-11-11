from django.db.models import Choices

class MediaTypes(Choices):
    VIDEO = 'Video'
    IMAGE = 'Image'
