from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^work/$', views.do_some_work, name='do_some_work'),
    url(r'^calcular/$', views.saca_numeros_sacar_palabras, name='saca_numeros_sacar_palabras'),
]