from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pets$', views.pet_score),
    url(r'^influx', views.influx, name= 'influx'),
]
