
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post",views.create_post,name="create_post"),
    path("like",views.like,name="like"),
    path("profile/<int:profile_id>",views.profile,name="profile"),
    path("follow/<int:profile_id>/<int:special_key>",views.follow,name="follow"),
    path("following",views.following,name="following"),
    path("edit",views.edit_post,name="edit")
]
