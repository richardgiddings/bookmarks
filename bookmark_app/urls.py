from django.conf.urls import url
from . import views

app_name = 'bookmarks'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^links/$', views.links, name='links'),
]