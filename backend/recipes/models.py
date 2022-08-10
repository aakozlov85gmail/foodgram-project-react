from django.db import models
from django.core.validators import MinValueValidator


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientRecipe',
    )
    image = models.ImageField(
        verbose_name='фото',
        upload_to='recipes/',
        blank=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=MinValueValidator(1,
                                     message='Время приготовления не может быть меньше 1 минуты'
                                     ))


class Tag(models.Model):
    """Модель тэга."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX код',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Ссылка',
        unique=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингериента."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Связующуя модель количества ингредиентов в рецепте."""

    pass


class Favorite(models.Model):
    """Модель избранных рецептов."""

    pass


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    pass
