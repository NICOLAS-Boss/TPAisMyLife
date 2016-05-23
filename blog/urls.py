from django.conf.urls import url, patterns, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'posts',views.PostViewSet)
router.register(r'profiles',views.ProfileViewSet)


urlpatterns = [
        url(r'^api/', include(router.urls)),
        url(r'^$',views.main, name='main'),
        url(r'^contacts/$',views.contacts, name='contacts'),
        url(r'^new_user/$',views.new_user,name='new_user'),
        url(r'^profile/$',views.profile_redirect,name='profile_redirect'),
        url(r'^profile/(?P<name>[a-zA-Z0-9]+)/$',views.profile, name='profile'),
        url(r'^profile/(?P<name>[a-zA-Z0-9]+)/(?P<num>\d+)/$',views.profile, name='profile'),
        url(r'^profile/new_post/$', views.new_post, name='new_post'),
        url(r'^new_profile/$', views.new_profile, name='new_profile'),
        url(r'^post/(?P<num>\d+)/$',views.post, name='post'),
        url(r'^post/add_like/(?P<num>\d+)/$',views.like_post, name='like_post'),
        url(r'statistics/$', views.statistics,name='statistics')
]
