from django.conf.urls import url

from uploads import views


app_name = 'uploads'

urlpatterns = [
    url(r'^upload$', views.UploadView.as_view(), name='new'),
]
