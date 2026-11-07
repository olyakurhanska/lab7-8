
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate

from forms import BookForm
from models import db, Author, Category, Book, BookDetail

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "local-development-key"
)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + (BASE_DIR / "books.sqlite3").as_posix()
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

BOOKS = [
    "Кобзар",
    "Лісова пісня",
    "Тіні забутих предків",
    "Місто",
]


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}


@app.route("/")
def home():
    return render_template(
        "home.html",
        title="Каталог книг",
        count=len(BOOKS),
        books=BOOKS
    )


@app.route("/books/")
def book_list():
    return render_template(
        "book_list.html",
        title="Список книг",
        count=len(BOOKS),
        books=BOOKS
    )


@app.route("/add/", methods=["GET", "POST"])
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        flash("Пропозицію книги успішно надіслано!", "success")
        return redirect(url_for("add_book"))

    return render_template("add_book.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
