from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


# @method_decorator(cache_page(240 * 60), name='dispatch')
class HeroView(TemplateView):
    template_name = 'pages/home.html'

    def post(self, request, **kwargs):
        return JsonResponse({'success': 'success'})
