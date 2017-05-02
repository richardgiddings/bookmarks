from django.conf.urls import url
from . import views

app_name = 'bookmarks'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^links/(?P<section_id>\d+)$', views.links, name='links'),

    url(r'^add_list/$', views.add_list, name='add_list'),
    url(r'^edit_list/(?P<list_id>\d+)$', views.edit_list, name='edit_list'),

    url(r'^add_section/(?P<list_id>\d+)$', views.add_section, name='add_section'),
    url(r'^edit_section/(?P<section_id>\d+)$', views.edit_section, name='edit_section'),
    url(r'^delete_section/$', views.delete_section, name='delete_section'),

    url(r'^add_link/(?P<section_id>\d+)$', views.add_link, name='add_link'),
    url(r'^edit_link/(?P<link_id>\d+)$', views.edit_link, name='edit_link'),
    url(r'^delete_link/$', views.delete_link, name='delete_link'),
]