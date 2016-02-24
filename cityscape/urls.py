from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pets$', views.pet_score),
    url(r'^influx', views.influx, name= 'influx'),
    url(r'^yell', views.yell, name='yell'),
    url(r'^traffic', views.traffic, name='traffic')
]
