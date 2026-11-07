
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class BookForm(FlaskForm):
    title = StringField(
        "Назва книги",
        validators=[
            DataRequired(message="Введіть назву книги."),
            Length(min=2, max=100,
                   message="Назва має містити від 2 до 100 символів.")
        ]
    )

    email = EmailField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Введіть правильну електронну адресу.")
        ]
    )

    genre = SelectField(
        "Жанр",
        choices=[
            ("", "Оберіть жанр"),
            ("novel", "Роман"),
            ("poetry", "Поезія"),
            ("fantasy", "Фентезі"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть жанр.")
        ]
    )

    description = TextAreaField(
        "Опис книги",
        validators=[
            DataRequired(message="Введіть опис книги.")
        ]
    )

    def validate_description(self, field):
        if len(field.data.split()) < 5:
            raise ValidationError(
                "Опис повинен містити щонайменше 5 слів."
            )
