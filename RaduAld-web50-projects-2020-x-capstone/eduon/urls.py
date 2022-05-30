
from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("", views.classes_view, name="index"),
    #Student/Parent
    path("class/<int:class_id>", views.class_view, name="class"),
    path("grades", views.grades_view, name="grades"),

    #Teacher
    path("create_subject", views.create_subject, name="create_subject"),
    path("your_class", views.your_class, name="your_class"),
]