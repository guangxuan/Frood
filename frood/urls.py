from django.conf.urls import patterns, url
from frood import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^meetup/(?P<meetup_name_url>\w+)/$', views.meetup, name='meetup'),
        url(r'^meetup/(?P<meetup_name_url>\w+)/join/$', views.meetup_join, name='meetup_join'),
        url(r'^meetup/(?P<meetup_name_url>\w+)/quit/$', views.meetup_quit, name='meetup_quit'),
        url(r'^meetup/(?P<meetup_name_url>\w+)/delete/$', views.meetup_delete, name='meetup_delete'),
        url(r'^add_meetup/(?P<xcor>-?\d+\.\d+)/(?P<ycor>-?\d+\.\d+)/$', views.add_meetup, name='add_meetup'), # NEW MAPPING!
        url(r'^select_location/$', views.select_location, name='select_location'), # NEW MAPPING!
        #url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'), 
        url(r'^register/$', views.register, name='register'),
        url(r'^restricted/', views.restricted, name='restricted'), #View that requires users to login
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^u/(?P<username>\w+)/$', views.user_profile, name='userprofile'),
        url(r'^u/(?P<tusername>\w+)/add_review/$', views.add_review, name='add_review')
)
