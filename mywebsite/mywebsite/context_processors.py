from django.conf import settings
from django.utils import translation


def i18n(request):
    return {
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGE_CODE': translation.get_language(),
        'LANGUAGE_BIDI': translation.get_language_bidi(),
    }
