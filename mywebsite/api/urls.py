from django.urls import re_path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

urlpatterns = router.urls

# urlpatterns.append(re_path(r'^product/(?P<pk>\d+)$', views.ProductExample.as_view(), name='api_product'))
# urlpatterns.append(re_path(r'^product/(?P<pk>\d+)/delete$', views.DeleteProductExample.as_view(), name='api_delete_product'))
# urlpatterns.append(re_path(r'^product/create$', views.CreateProductExample.as_view(), name='api_create_product'))
# urlpatterns.append(re_path(r'^products$', views.ProductsExample.as_view(), name='api_products'))

# urlpatterns.append(re_path(r'^dashboard/settings$', views.DashboardSettingsView.as_view(), name='api_settings'))

# urlpatterns.append(re_path(r'^dashboard/users/(?P<pk>\d+)/actions$', views.UserActionsView.as_view(), name='api_user_actions'))
# urlpatterns.append(re_path(r'^dashboard/users/(?P<pk>\d+)/(?P<product>\d+)/message$', views.MessageUserView.as_view(), name='api_send_message'))
# urlpatterns.append(re_path(r'^dashboard/users/(?P<pk>\d+)/rate$', views.RateUserView.as_view(), name='api_user_rate'))
