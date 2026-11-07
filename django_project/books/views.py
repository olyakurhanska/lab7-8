
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookForm

BOOKS = [
    "Кобзар",
    "Лісова пісня",
    "Тіні забутих предків",
    "Місто",
]


def home(request):
    context = {
        "title": "Каталог книг",
        "count": len(BOOKS),
        "books": BOOKS,
    }
    return render(request, "books/home.html", context)


def book_list(request):
    context = {
        "title": "Список книг",
        "count": len(BOOKS),
        "books": BOOKS,
    }
    return render(request, "books/book_list.html", context)


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            messages.success(
                request,
                "Пропозицію книги успішно надіслано!"
            )
            return redirect("add_book")
    else:
        form = BookForm()

    return render(
        request,
        "books/add_book.html",
        {"form": form}
    )
