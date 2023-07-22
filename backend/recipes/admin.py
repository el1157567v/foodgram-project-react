from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                     ShoppingCart, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Управление рецептами в admin."""

    list_display = ('id', 'name', 'author', 'text', 'cooking_time', 'pub_date')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Управление тегами в admin."""

    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Управление ингредиентами в admin."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    """Управление ингредиентами в рецептах в admin."""

    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Управление избранными рецептами в admin."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Управление корзиной покупок в admin."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'
