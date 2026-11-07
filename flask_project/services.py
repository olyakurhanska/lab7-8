
import smtplib
from datetime import datetime
from email.message import EmailMessage


def get_current_year():
    return datetime.now().year


def send_book_notification(recipient, book_title):
    message = EmailMessage()
    message["From"] = "catalog@example.com"
    message["To"] = recipient
    message["Subject"] = "Нова пропозиція книги"
    message.set_content(
        f"До каталогу запропоновано книгу: {book_title}"
    )

    with smtplib.SMTP("localhost", 1025, timeout=5) as smtp:
        smtp.send_message(message)
