from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^influx', views.influx, name= 'influx'),
    url(r'^yelling', views.yelling, name='yelling'),

]
    
