from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^pets$', views.pet_score),
    url(r'^chart$', views.chart, name='chart'),
    url(r'^traffic', views.traffic, name='traffic')
]
