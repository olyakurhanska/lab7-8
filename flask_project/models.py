
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


book_categories = db.Table(
    "book_categories",
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id"),
        primary_key=True
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("category.id"),
        primary_key=True
    )
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.Integer, nullable=True)

    books = db.relationship(
        "Book",
        backref="author",
        lazy=True
    )

    def __str__(self):
        return self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, default="")
    is_active = db.Column(db.Boolean, default=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("author.id"),
        nullable=False
    )

    publication_year = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    rating = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    categories = db.relationship(
        "Category",
        secondary=book_categories,
        backref="books",
        lazy=True
    )

    def __str__(self):
        return self.title


class BookDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    isbn = db.Column(db.String(13), unique=True, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    language = db.Column(
        db.String(50),
        default="Українська"
    )

    book = db.relationship(
        "Book",
        backref=db.backref(
            "detail",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )

    def __str__(self):
        return f"Деталі: {self.book.title}"
