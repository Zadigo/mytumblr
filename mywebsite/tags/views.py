from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.cache import caches
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from tags import models


@method_decorator(cache_page(1 * 60), name='dispatch')
class VideosByTagView(LoginRequiredMixin, ListView):
    model = models.Tag
    template_name = 'pages/tags.html'
    context_object_name = 'videos'
    paginate_by = 100

    def get_queryset(self):
        try:
            tag = self.model.objects.get(title__exact=self.kwargs['tag'])
        except:
            queryset = []
        else:
            queryset = tag.video_set.filter(public=True)
        return queryset
