from django.conf.urls import url

from . import views

urlpatterns = [
<<<<<<< HEAD


    url(r'^traffic', views.traffic, name='traffic'),
    url(r'^yelling', views.yelling, name='yelling'),
=======
    # url(r'^weather', views.index, name='weather'),
>>>>>>> 223db0a2fcbac668667608e9bbc031b69e6ae54f
    url(r'^', views.index, name='index'),
]
