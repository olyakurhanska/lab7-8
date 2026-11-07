
import pytest
from sqlalchemy.exc import IntegrityError

from models import db, Author, Category, Book, BookDetail


def test_author_creation(author):
    assert author.name == "Тестовий автор"
    assert author.country == "Україна"


def test_author_str(author):
    assert str(author) == "Тестовий автор"


def test_book_default_values(author):
    book = Book(
        title="Книга без рейтингу",
        author=author,
        publication_year=2022
    )
    db.session.add(book)
    db.session.commit()

    assert book.rating == 0
    assert book.is_available is True


def test_book_relationship(book, author, category):
    assert book.author == author
    assert book in author.books
    assert category in book.categories


def test_book_detail_cascade(book):
    detail = BookDetail(
        book=book,
        isbn="9780000000003",
        pages=200,
        language="Українська"
    )
    db.session.add(detail)
    db.session.commit()

    detail_id = detail.id
    db.session.delete(book)
    db.session.commit()

    assert db.session.get(BookDetail, detail_id) is None


def test_category_unique(app):
    first = Category(name="Унікальна категорія")
    db.session.add(first)
    db.session.commit()

    second = Category(name="Унікальна категорія")
    db.session.add(second)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


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

    db.session.add(book)
    db.session.commit()

    assert book.rating == rating


def test_book_str(book):
    assert str(book) == "Тестова книга"
