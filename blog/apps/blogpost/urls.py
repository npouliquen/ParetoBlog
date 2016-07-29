from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<post_id>\d+)/$', views.single_post, name='single_post'),
    url(r'^post/new/$', views.new_post, name='new_post'),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^markdownx/', include('markdownx.urls')),
]
