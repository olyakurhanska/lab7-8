
from pathlib import Path

import pytest
from flask import Flask

from app import app as main_app, inject_year
from models import db, Author, Category, Book


BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def app():
    test_app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    test_app.config.update(
        TESTING=True,
        SECRET_KEY="testing-only-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
    )

    db.init_app(test_app)

    for rule in main_app.url_map.iter_rules():
        if rule.endpoint == "static":
            continue

        test_app.add_url_rule(
            rule.rule,
            endpoint=rule.endpoint,
            view_func=main_app.view_functions[rule.endpoint],
            methods=list(rule.methods),
        )

    test_app.context_processor(inject_year)

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def author(app):
    obj = Author(
        name="Тестовий автор",
        country="Україна",
        birth_year=1980,
    )
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def category(app):
    obj = Category(
        name="Тестова категорія",
        description="Категорія для тестів",
        is_active=True,
    )
    db.session.add(obj)
    db.session.commit()
    return obj


@pytest.fixture
def book(app, author, category):
    obj = Book(
        title="Тестова книга",
        author=author,
        publication_year=2020,
        rating=5,
    )
    obj.categories.append(category)
    db.session.add(obj)
    db.session.commit()
    return obj
