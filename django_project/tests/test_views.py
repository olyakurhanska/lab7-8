
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page(client):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "books/home.html" in [
        template.name for template in response.templates
    ]
    assert "Каталог книг" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_book_list_page(client):
    response = client.get(reverse("book_list"))

    assert response.status_code == 200
    assert "books/book_list.html" in [
        template.name for template in response.templates
    ]
    assert "Кобзар" in response.content.decode("utf-8")


def test_page_not_found(client):
    response = client.get("/unknown-page/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_add_book_page(client):
    response = client.get(reverse("add_book"))

    assert response.status_code == 200
    assert "books/add_book.html" in [
        template.name for template in response.templates
    ]
    assert "form" in response.context


@pytest.mark.django_db
def test_add_book_valid_post(client):
    response = client.post(
        reverse("add_book"),
        {
            "title": "Тестова книга",
            "email": "test@example.com",
            "genre": "novel",
            "description": "Це цікава тестова книга про пригоди.",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("add_book")


@pytest.mark.django_db
def test_add_book_invalid_post(client):
    response = client.post(
        reverse("add_book"),
        {
            "title": "Тестова книга",
            "email": "test@example.com",
            "genre": "novel",
            "description": "Два слова",
        },
    )

    assert response.status_code == 200
    assert "Опис повинен містити" in response.content.decode("utf-8")
