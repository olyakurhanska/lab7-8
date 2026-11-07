
from django import forms


class BookForm(forms.Form):
    title = forms.CharField(
        label="Назва книги",
        max_length=100,
        min_length=2,
        error_messages={
            "required": "Введіть назву книги.",
            "min_length": "Назва має містити щонайменше 2 символи.",
        },
    )

    email = forms.EmailField(
        label="Електронна пошта",
        error_messages={
            "required": "Введіть електронну пошту.",
            "invalid": "Введіть правильну електронну адресу.",
        },
    )

    genre = forms.ChoiceField(
        label="Жанр",
        choices=[
            ("", "Оберіть жанр"),
            ("novel", "Роман"),
            ("poetry", "Поезія"),
            ("fantasy", "Фентезі"),
            ("other", "Інше"),
        ],
    )

    description = forms.CharField(
        label="Опис книги",
        widget=forms.Textarea(attrs={"rows": 4}),
        error_messages={
            "required": "Введіть опис книги.",
        },
    )

    def clean_description(self):
        description = self.cleaned_data["description"]

        if len(description.split()) < 5:
            raise forms.ValidationError(
                "Опис повинен містити щонайменше 5 слів."
            )

        return description
