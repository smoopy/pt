from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='home'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^about/$', views.about, name='about'),
]
