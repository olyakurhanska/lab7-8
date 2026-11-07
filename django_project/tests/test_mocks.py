
from datetime import datetime
from unittest.mock import patch

from books.services import get_current_year, send_book_notification


def test_external_email_mock():
    with patch("books.services.send_mail") as mock_send:
        send_book_notification("test@example.com", "Кобзар")

        mock_send.assert_called_once_with(
            "Нова пропозиція книги",
            "До каталогу запропоновано книгу: Кобзар",
            "catalog@example.com",
            ["test@example.com"],
            fail_silently=False,
        )


def test_internal_datetime_mock():
    fixed_date = datetime(2026, 11, 7)

    with patch("books.services.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_date

        result = get_current_year()

        mock_datetime.now.assert_called_once_with()
        assert result == 2026
