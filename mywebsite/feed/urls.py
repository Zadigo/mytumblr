from django.conf.urls import url

from feed import views

app_name = 'feed'

urlpatterns = [
    url(r'^test-feed-more$', views.test_timeline_more, name='test_timeline_more'),
    url(r'^test-feed$', views.test_timeline, name='test_timeline'),

    url(r'^add-comment$', views.create_comment, name='comment'),
    url(r'^add-like$', views.add_like, name='like'),
    
    # url(r'^u/(?P<username>[a-z]+)/followers$', views.FollowersView.as_view(), name='followers'),
    # url(r'^u/(?P<username>[a-z]+)/follows$', views.FollowsView.as_view(), name='follows'),

    url(r'^u/(?P<username>[a-z]+)/unfollow$', views.unfollow_user, name='unfollow'),
    url(r'^u/(?P<username>[a-z]+)/follow$', views.follow_user, name='follow'),
    url(r'^u/(?P<username>\w+)$', views.UserTimeLine.as_view(), name='user_timeline'),
    
    url(r'^report$', views.report, name='report'),
    url(r'^search$', views.SearchView.as_view(), name='search'),
    url(r'^$', views.TimeLineView.as_view(), name='timeline')
]
