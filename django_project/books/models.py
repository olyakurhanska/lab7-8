
from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Ім'я автора"
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Країна"
    )
    birth_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Рік народження"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Назва категорії"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Опис категорії"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Назва книги"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="books",
        verbose_name="Автор"
    )
    categories = models.ManyToManyField(
        Category,
        related_name="books",
        verbose_name="Категорії"
    )
    publication_year = models.PositiveIntegerField(
        verbose_name="Рік видання"
    )
   
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступна"
    )

    rating = models.PositiveIntegerField(
        default=0,
        verbose_name="Рейтинг книги"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class BookDetail(models.Model):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        related_name="detail",
        verbose_name="Книга"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="ISBN"
    )
    pages = models.PositiveIntegerField(
        verbose_name="Кількість сторінок"
    )
    language = models.CharField(
        max_length=50,
        default="Українська",
        verbose_name="Мова"
    )

    class Meta:
        ordering = ["book__title"]
        verbose_name = "Деталі книги"
        verbose_name_plural = "Деталі книг"

    def __str__(self):
        return f"Деталі: {self.book.title}"
