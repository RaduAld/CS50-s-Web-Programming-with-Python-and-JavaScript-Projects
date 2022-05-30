from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.page, name="page"),
    path("create_page/", views.create, name="create"),
    path("wiki/<str:title>/edit_page/", views.edit, name="edit"),
    path("random/", views.rdm, name="random"),
]