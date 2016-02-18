from django.conf.urls import url

from . import views

urlpatterns = [


    url(r'^traffic', views.traffic, name='traffic'),
    url(r'^yelling', views.yelling, name='yelling'),
    url(r'^', views.index, name='index'),

]
