from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^weather', views.index, name='weather'),
    url(r'^$', views.index, name='index'),
    url(r'^', views.index, name='index'),

]
