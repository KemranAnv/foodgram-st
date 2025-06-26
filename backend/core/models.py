from django.db import models
from django.core.validators import RegexValidator


class Ingredient(models.Model):
    """
    Model to represent an ingredient.
    This can be used to store information about ingredients used in recipes.
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        unique=True,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, ({self.measurement_unit})'


class Tag(models.Model):
    """
    Model to represent a tag.
    This can be used to categorize recipes with tags.
    """
    name = models.CharField(
        'Название тега',
        max_length=100,
        unique=True,
    )
    color = models.CharField(
        'Цвет (HEX)',
        max_length=7,
        validators=[
            RegexValidator(
                r'^#([A-Fa-f0-9]{6})$',
                'Цвет должен быть в формате #RRGGBB',
            )
        ],
    )
    slug = models.SlugField(
        'Слаг',
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
