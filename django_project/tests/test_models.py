
import pytest
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError

from books.models import Author, Category, Book, BookDetail


pytestmark = pytest.mark.django_db


def test_author_creation(author):
    assert author.name == "Тестовий автор"
    assert author.country == "Україна"


def test_author_str(author):
    assert str(author) == "Тестовий автор"


def test_book_default_value(author):
    book = Book.objects.create(
        title="Книга без рейтингу",
        author=author,
        publication_year=2022
    )
    assert book.rating == 0
    assert book.is_available is True


def test_book_relationship(book, author, category):
    assert book.author == author
    assert category in book.categories.all()
    assert book in author.books.all()


def test_book_detail_cascade(book):
    detail = BookDetail.objects.create(
        book=book,
        isbn="9780000000003",
        pages=200
    )
    detail_id = detail.id

    book.delete()

    assert not BookDetail.objects.filter(
        id=detail_id
    ).exists()


def test_author_protected_delete(author, book):
    with pytest.raises(ProtectedError):
        author.delete()

    assert Author.objects.filter(
        id=author.id
    ).exists()


@pytest.mark.parametrize(
    "rating",
    [0, 1, 3, 5, 10]
)
def test_book_rating_values(author, rating):
    book = Book(
        title="Книга з рейтингом",
        author=author,
        publication_year=2020,
        rating=rating
    )

    book.full_clean()

    assert book.rating == rating


def test_book_title_max_length(author):
    book = Book(
        title="А" * 201,
        author=author,
        publication_year=2020
    )

    with pytest.raises(ValidationError):
        book.full_clean()
