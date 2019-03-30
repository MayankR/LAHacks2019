from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('msg', views.msg, name='msg'),
	# path('test', views.test, name='test'),
]