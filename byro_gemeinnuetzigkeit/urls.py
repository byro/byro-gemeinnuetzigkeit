from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^members/view/(?P<pk>\d+)/bescheinigung$', views.Bescheinigung.as_view(), name='members.bescheinigung'),
]
