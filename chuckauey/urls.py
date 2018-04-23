from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^canpark/$', views.CanPark.as_view(), name='list'),
    url(r'^findpark/$', views.FindPark.as_view(), name='list'),
    #url(r'^(?P<string>[\w\-]+)/$', views.ListUsers.as_view(), name='list')
]