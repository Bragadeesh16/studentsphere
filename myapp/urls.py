from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("groups", views.groups_list, name="group-list"),
]
