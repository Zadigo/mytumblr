from django.conf.urls import url

from notifications import views

app_name = 'notifications'

urlpatterns = [
    url(r'^u/(?P<username>[a-z]+)/get$', views.get_notifications, name='get_notifications'),
    url(r'^$', views.NotificationsView.as_view(), name='home')
]
