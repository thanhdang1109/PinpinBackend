from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<username>[a-zA-Z0-9_]+)/new_video/$', views.save_new_video),
    url(r'(?P<username>[a-zA-Z0-9_]+)/videos/$', views.get_user_videos),
    url(r'(?P<username>[a-zA-Z0-9_]+)/delete_video/$', views.delete_video),
    url(r'(?P<username>[a-zA-Z0-9_]+)/new_following/$', views.new_following),
    url(r'(?P<username>[a-zA-Z0-9_]+)/unfollowing/$', views.unfollowing),
    url(r'(?P<username>[a-zA-Z0-9_]+)/feeds/$', views.following_feeds),
    url(r'(?P<city_name>[a-zA-Z]+)/users/$', views.find_users_in_location),
    url(r'^$', views.index),
]
