from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


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
        validators=MinValueValidator(
            1,
            message='Время приготовления не может быть меньше 1 минуты'
        )
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Связующуя модель количества ингредиентов в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=MinValueValidator(
            1,
            message='Ингредиентов должно быть не менее 1 единицы'
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class Favorite(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Корзина покупок'
