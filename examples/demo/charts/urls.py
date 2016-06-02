from django.conf.urls import url

from charts import views


urlpatterns = [
    url(r'^$', views.charts, name='charts'),
]
