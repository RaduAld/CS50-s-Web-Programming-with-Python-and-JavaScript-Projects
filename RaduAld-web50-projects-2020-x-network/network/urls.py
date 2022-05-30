
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    #API Routes
    path("posts", views.posts, name="posts"),
    path("posts/<int:post_id>", views.post_view, name="post_view"),
    path("user/<str:username>", views.user, name="user"),
]
