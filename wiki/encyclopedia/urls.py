from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.show_entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("save/", views.save, name="save"),
    path("edit/<str:title>/", views.edit, name="edit")
]
