
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db.models import Q, Count, Avg
from books.models import Author, Category, Book, BookDetail


print("=== 1. СТВОРЕННЯ ДАНИХ ===")

author, _ = Author.objects.get_or_create(
    name="Демо автор ORM",
    defaults={
        "country": "Україна",
        "birth_year": 1980,
    }
)

category, _ = Category.objects.get_or_create(
    name="Демо категорія ORM",
    defaults={
        "description": "Навчальна категорія",
        "is_active": True,
    }
)

book, _ = Book.objects.update_or_create(
    title="Демо книга ORM",
    author=author,
    defaults={
        "publication_year": 2020,
        "is_available": True,
        "rating": 5,
    }
)

book.categories.add(category)

BookDetail.objects.update_or_create(
    book=book,
    defaults={
        "isbn": "9780000000001",
        "pages": 250,
        "language": "Українська",
    }
)

print("Створено або оновлено:", book.title)


print("\n=== 2. CRUD ===")

# CREATE
Book.objects.filter(
    title="Тимчасова тестова книга",
    author=author
).delete()

temp_book = Book.objects.create(
    title="Тимчасова тестова книга",
    author=author,
    publication_year=2021,
    rating=3
)
print("CREATE:", temp_book.title)

# READ
found = Book.objects.get(pk=temp_book.pk)
print("READ:", found.title)

# UPDATE
found.rating = 4
found.save()
print("UPDATE: рейтинг =", found.rating)

# DELETE
found.delete()
print("DELETE: тимчасову книгу видалено")


print("\n=== 3. FILTER ===")

for item in Book.objects.filter(is_available=True):
    print(item.title)


print("\n=== 4. EXCLUDE ===")

for item in Book.objects.exclude(rating=0):
    print(item.title)


print("\n=== 5. Q-ОБ'ЄКТИ ===")

results = Book.objects.filter(
    Q(rating__gte=4) | Q(publication_year__gte=2020)
)

for item in results:
    print(item.title)


print("\n=== 6. AGGREGATE ===")

statistics = Book.objects.aggregate(
    total=Count("id"),
    average_rating=Avg("rating")
)

print(statistics)


print("\n=== 7. ANNOTATE ===")

authors = Author.objects.annotate(
    book_count=Count("books")
)

for item in authors:
    print(item.name, "— книг:", item.book_count)


print("\n=== 8. ЗВОРОТНІ ЗВ'ЯЗКИ ===")

for item in author.books.all():
    print("Автор:", author.name, "Книга:", item.title)


print("\n=== 9. SELECT_RELATED ===")

books = Book.objects.select_related("author")

for item in books:
    print(item.title, "—", item.author.name)


print("\n=== 10. PREFETCH_RELATED ===")

books = Book.objects.prefetch_related("categories")

for item in books:
    names = [c.name for c in item.categories.all()]
    print(item.title, "— категорії:", names)


print("\nУсі операції Django ORM виконано.")
