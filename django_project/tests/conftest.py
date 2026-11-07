
import pytest
from django.contrib.auth import get_user_model
from books.models import Author, Category, Book


@pytest.fixture
def test_user(db):
    return get_user_model().objects.create_user(
        username="test_reader",
        password="TestPassword123!"
    )


@pytest.fixture
def author(db):
    return Author.objects.create(
        name="Тестовий автор",
        country="Україна",
        birth_year=1980
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Тестова категорія",
        description="Категорія для тестів",
        is_active=True
    )


@pytest.fixture
def book(db, author, category):
    new_book = Book.objects.create(
        title="Тестова книга",
        author=author,
        publication_year=2020,
        rating=5
    )
    new_book.categories.add(category)
    return new_book
