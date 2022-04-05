
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submit", views.submit, name="submit"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow/<int:user_to_follow>", views.follow, name="follow"),
    path("unfollow/<int:user_to_unfollow>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("page/<int:page_num>", views.page, name="page"),
    path("profile/<int:user_id>/page/<int:profile_page>", views.profile_page, name="profile_page"),
    path("following/page/<int:following_page>", views.following_page, name="following_page"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("page/edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/edit/<int:post_id>", views.edit, name="edit"),
]
