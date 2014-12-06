from django.conf.urls import patterns, url

from library import views

urlpatterns = patterns('',
                       url(r'^$',
                           views.index,
                           name='index'),
                       url(r'^search/$',
                           views.SearchView.as_view(),
                           name='search'),
                       )
