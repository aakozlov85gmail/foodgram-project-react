from django.contrib import admin

from .models import Recipe, Tag, Ingredient, IngredientRecipe, Favorite, ShoppingCart


class FavoriteRecipes(admin.TabularInline):
    model = Favorite


class RecipeAdmin(admin.ModelAdmin):
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
    inlines = [FavoriteRecipes, ]

    def favorites_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    favorites_count.short_description = 'В избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
