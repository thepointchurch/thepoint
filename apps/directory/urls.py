from django.conf.urls import patterns, url

from directory import views

urlpatterns = patterns('',
                       url(r'^$',
                           views.IndexView.as_view(),
                           name='index'),
                       url(r'^(?P<letter>[a-z])/$',
                           views.LetterView.as_view(),
                           name='letter'),
                       url(r'^(?P<pk>\d+)/$',
                           views.DetailView.as_view(),
                           name='detail'),
                       url(r'^search/$',
                           views.SearchView.as_view(),
                           name='search'),
                       url(r'^edit/$',
                           views.FamilyEditView.as_view(),
                           name='edit'),
                       url(r'^birthdays/$',
                           views.BirthdayView.as_view(),
                           name='birthdays'),
                       url(r'^anniversaries/$',
                           views.AnniversaryView.as_view(),
                           name='anniversaries'),
                       )