from django.http import Http404
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import status

from .serializers import RecipeListSerializer


def create_recipe_user(request, pk, model):
    """Доп.функция: создаем связку рецепт<->пользователь по id рецепта."""
    recipe = get_object_or_404(Recipe, id=pk)
    obj, created = model.objects.get_or_create(
        recipe=recipe,
        user=request.user
    )
    if not created:
        return (
            {"errors": f"Уже есть рецепт с id {pk}."},
            status.HTTP_400_BAD_REQUEST
        )
    serializer = RecipeListSerializer(
        recipe,
        context={'request': request}
    )
    return (serializer.data, status.HTTP_201_CREATED)


def delete_recipe_user(request, pk, model):
    """Доп.функция: удаляем связку рецепт<->пользователь по id рецепта."""
    recipe = get_object_or_404(Recipe, id=pk)
    try:
        favorite_recipe = model.objects.get(recipe=recipe, user=request.user)
        favorite_recipe.delete()
        return (
            {"message": f"Рецепт с id {pk} удален."},
            status.HTTP_204_NO_CONTENT
        )
    except model.DoesNotExist:
        raise Http404
