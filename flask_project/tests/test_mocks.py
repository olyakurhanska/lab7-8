
from datetime import datetime
from unittest.mock import patch

from services import get_current_year, send_book_notification


def test_external_email_mock():
    with patch("services.smtplib.SMTP") as mock_smtp:
        send_book_notification(
            "test@example.com",
            "Кобзар"
        )

        mock_smtp.assert_called_once_with(
            "localhost", 1025, timeout=5
        )

        connection = mock_smtp.return_value.__enter__.return_value
        connection.send_message.assert_called_once()

        message = connection.send_message.call_args.args[0]
        assert message["To"] == "test@example.com"
        assert "Кобзар" in message.get_content()


def test_internal_datetime_mock():
    fixed_date = datetime(2026, 11, 7)

    with patch("services.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_date

        result = get_current_year()

        mock_datetime.now.assert_called_once_with()
        assert result == 2026
