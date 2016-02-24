from django.conf.urls import url

from . import views
from . import happy

urlpatterns = [
    # url(r'^weather', views.index, name='weather'),
    url(r'^$', views.index, name='index'),
    url(r'^chart$', views.chart, name='chart'),
]
