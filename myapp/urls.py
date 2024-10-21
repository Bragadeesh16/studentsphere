from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("groups", views.groups_list, name="group-list"),
    path("cse-second-year", views.Cse_second, name="cse_second"),
    path(
        "cse-second-year/remove meember",
        views.cse_two_remove_member,
        name="cse_second_remove_memeber",
    ),
    path("cse-third", views.Cse_third, name="cse_third"),
    path(
        "cse-third-year/remove meember",
        views.cse_three_remove_member,
        name="cse_three_remove_memeber",
    ),
    path("cse-fourth-year", views.Cse_four, name="cse_fourth"),
    path(
        "cse-fourth-year/remove member",
        views.cse_fourth_remove_member,
        name="cse_four_remove_member",
    ),
    
]
