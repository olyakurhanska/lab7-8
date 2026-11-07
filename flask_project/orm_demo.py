
from app import app
from models import db, Author, Category, Book, BookDetail
from sqlalchemy import select, func, or_


def run_demo():
    with app.app_context():

        print("=== 1. СТВОРЕННЯ ДАНИХ ===")

        author = db.session.scalar(
            select(Author).filter_by(name="Демо автор Flask ORM")
        )

        if author is None:
            author = Author(
                name="Демо автор Flask ORM",
                country="Україна",
                birth_year=1980
            )
            db.session.add(author)

        category = db.session.scalar(
            select(Category).filter_by(name="Демо категорія Flask")
        )

        if category is None:
            category = Category(
                name="Демо категорія Flask",
                description="Навчальна категорія",
                is_active=True
            )
            db.session.add(category)

        book = db.session.scalar(
            select(Book).filter_by(
                title="Демо книга Flask ORM",
            )
        )

        if book is None:
            book = Book(
                title="Демо книга Flask ORM",
                author=author,
                publication_year=2020,
                is_available=True,
                rating=5
            )
            db.session.add(book)

        if category not in book.categories:
            book.categories.append(category)

        db.session.flush()

        detail = db.session.scalar(
            select(BookDetail).filter_by(book_id=book.id)
        )

        if detail is None:
            detail = BookDetail(
                book=book,
                isbn="9780000000002",
                pages=250,
                language="Українська"
            )
            db.session.add(detail)

        db.session.commit()

        print("Створено або знайдено:", book.title)
        print("COMMIT: пов'язані дані збережено")


        print("\n=== 2. CRUD ===")

        temp = Book(
            title="Тимчасова книга Flask",
            author=author,
            publication_year=2021,
            rating=3
        )

        db.session.add(temp)
        db.session.commit()
        temp_id = temp.id
        print("CREATE:", temp.title)

        found = db.session.get(Book, temp_id)
        print("READ:", found.title)

        found.rating = 4
        db.session.commit()
        print("UPDATE: рейтинг =", found.rating)

        db.session.delete(found)
        db.session.commit()

        deleted = db.session.get(Book, temp_id)
        print("DELETE:", deleted is None)


        print("\n=== 3. FILTER ===")

        books = db.session.scalars(
            select(Book).where(Book.is_available.is_(True))
        ).all()

        for item in books:
            print(item.title)


        print("\n=== 4. СКЛАДНА УМОВА OR ===")

        books = db.session.scalars(
            select(Book).where(
                or_(
                    Book.rating >= 4,
                    Book.publication_year >= 2020
                )
            )
        ).all()

        for item in books:
            print(item.title)


        print("\n=== 5. АГРЕГАЦІЯ ===")

        total, average = db.session.execute(
            select(
                func.count(Book.id),
                func.avg(Book.rating)
            )
        ).one()

        print("Кількість книг:", total)
        print("Середній рейтинг:", average)


        print("\n=== 6. ЗВ'ЯЗКИ ===")

        print("Автор:", book.author.name)
        print("Категорії:", [c.name for c in book.categories])
        print("Деталі:", book.detail.isbn)


        print("\n=== 7. ТРАНЗАКЦІЯ ROLLBACK ===")

        rollback_book = Book(
            title="Книга для rollback Flask",
            author=author,
            publication_year=2022,
            rating=2
        )

        db.session.add(rollback_book)
        db.session.flush()

        rollback_id = rollback_book.id
        print("До rollback: запис підготовлено")

        db.session.rollback()

        result = db.session.get(Book, rollback_id)

        print("Після rollback: запис відсутній =", result is None)

        print("\nУсі операції Flask ORM виконано.")


if __name__ == "__main__":
    run_demo()
