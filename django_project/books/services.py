
from datetime import datetime
from django.core.mail import send_mail


def get_current_year():
    return datetime.now().year


def send_book_notification(recipient, book_title):
    return send_mail(
        "Нова пропозиція книги",
        f"До каталогу запропоновано книгу: {book_title}",
        "catalog@example.com",
        [recipient],
        fail_silently=False,
    )
