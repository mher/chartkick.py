from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'charts.views.charts', name='charts'),
)
