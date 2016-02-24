from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^traffic', views.traffic, name='traffic'),
    url(r'^yell', views.yell, name='yell'),

    # url(r'^weather', views.index, name='weather'),

    url(r'^', views.index, name='index'),

    url(r'^influx', views.influx, name= 'influx'),
