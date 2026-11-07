
from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("add/", views.add_book, name="add_book"),
]
