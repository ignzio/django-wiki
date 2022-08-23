from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.wiki_entry, name='wiki_entry'),
    path(r"^page-not-found/$", views.notFound, name="notFound"),
    path('search', views.search_entry, name="search"),
    path('new-entry', views.make_new_entry, name="new_entry"),
    path('wiki/<str:title>/edit', views.edit_entry, name="edit_entry"),
    path('wiki/save-edit', views.save_edit, name='save_edit'),
    path("random-page", views.random_page, name="random_page")
]
