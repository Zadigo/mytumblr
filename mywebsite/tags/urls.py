from django.conf.urls import url

from tags import views

app_name = 'tags'

urlpatterns = [
    url(r'^(?P<tag>\w+)$', views.VideosByTagView.as_view(), name='tag'),
]
