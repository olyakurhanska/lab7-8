
import re


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Каталог книг" in response.get_data(as_text=True)


def test_book_list_page(client):
    response = client.get("/books/")

    assert response.status_code == 200
    assert "Кобзар" in response.get_data(as_text=True)


def test_page_not_found(client):
    response = client.get("/unknown-page/")

    assert response.status_code == 404


def test_add_book_page(client):
    response = client.get("/add/")

    assert response.status_code == 200
    assert "Запропонувати книгу" in response.get_data(
        as_text=True
    )
    assert 'name="csrf_token"' in response.get_data(
        as_text=True
    )


def get_csrf_token(client):
    response = client.get("/add/")
    html = response.get_data(as_text=True)

    match = re.search(
        r'name="csrf_token"[^>]*value="([^"]+)"',
        html
    )

    assert match is not None
    return match.group(1)


def test_add_book_valid_post(client):
    token = get_csrf_token(client)

    response = client.post(
        "/add/",
        data={
            "csrf_token": token,
            "title": "Тестова книга",
            "email": "test@example.com",
            "genre": "novel",
            "description": "Це цікава тестова книга про пригоди.",
        },
    )

    assert response.status_code == 302
    assert response.location.endswith("/add/")


def test_add_book_invalid_post(client):
    token = get_csrf_token(client)

    response = client.post(
        "/add/",
        data={
            "csrf_token": token,
            "title": "Тестова книга",
            "email": "test@example.com",
            "genre": "novel",
            "description": "Два слова",
        },
    )

    assert response.status_code == 200
    assert "Опис повинен містити" in response.get_data(
        as_text=True
    )


def test_add_book_without_csrf(client):
    response = client.post(
        "/add/",
        data={
            "title": "Тестова книга",
            "email": "test@example.com",
            "genre": "novel",
            "description": "Це цікава тестова книга про пригоди.",
        },
    )

    assert response.status_code == 200
    assert "Пропозицію книги успішно надіслано" not in (
        response.get_data(as_text=True)
    )
