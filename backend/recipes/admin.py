from django.contrib import admin

from .models import (
    Recipe,
    Tag,
    Ingredient,
    IngredientRecipe,
    Favorite,
    ShoppingCart
)


class IngredientInline(admin.TabularInline):
    """Возможность добавления игредиента из модели рецепта в админке."""

    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Отображение модели Recipe в админке."""

    list_display = (
        'name',
        'author',
        'favorites_count',
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    readonly_fields = (
        'favorites_count',
    )
    inlines = (IngredientInline,)

    @admin.display(description='В избранном')
    def favorites_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображение модели Tag в админке."""

    list_display = (
        'name',
        'color',
        'slug',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Отображение модели Ingredient в админке."""

    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Отображение модели IngredientRecipe в админке."""

    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Отображение модели Favorite в админке."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Отображение модели ShoppingCart в админке."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user',)
