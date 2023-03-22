from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^members/view/(?P<pk>\d+)/bescheinigung/(?P<receipt>\d+)/send$",
        views.SendBescheinigung.as_view(),
        name="members.bescheinigung.send",
    ),
    url(
        r"^members/view/(?P<pk>\d+)/bescheinigung$",
        views.Bescheinigung.as_view(),
        name="members.bescheinigung",
    ),
]
