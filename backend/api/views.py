from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingCart, Tag)
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User

from .filters import IngredientFilter, RecipeFilter
from .paginators import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (ChangePasswordSerializer, CustomUserCreateSerializer,
                          CustomUserSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          SubscriptionSerializer, TagSerializer)


class CustomUserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Кастомный Viewset для пользователя."""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    """Viewset для подписки на авторов."""
    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        subscription = Subscription.objects.filter(user=request.user,
                                                   author=author).first()
        serializer = SubscriptionSerializer(author, data=request.data,
                                            context={'request': request})
        if request.method == 'DELETE' and subscription:
            subscription.delete()
            return Response({'message': 'Подписка на автора успешно удалена.'},
                            status=status.HTTP_204_NO_CONTENT)
        serializer.is_valid(raise_exception=True)
        Subscription.objects.create(user=request.user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CurrentUserMeView(views.APIView):
    """View для просмотра текущего пользователя (себя)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(
            request.user,
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(views.APIView):
    """View для изменения пароля."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = request.user
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Пароль успешно изменен.'},
                        status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для тега."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для ингредиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для рецепта."""
    queryset = Recipe.objects.prefetch_related(
        'author', 'tags', 'ingredients').all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """Viewset для избранного."""
    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        """Действия с избранным: добавляем/удаляем рецепт."""
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.filter(user=request.user,
                                           recipe=recipe).first()
        serializer = FavoriteSerializer(recipe, data=request.data,
                                        context={'request': request})
        if request.method == 'DELETE' and favorite:
            favorite.delete()
            return Response({'message': 'Рецепт успешно удален из избранного'},
                            status=status.HTTP_204_NO_CONTENT)
        serializer.is_valid(raise_exception=True)
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Viewset для корзины покупок."""
    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        """Действия с корзиной: добавляем/удаляем рецепт."""
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = ShoppingCart.objects.filter(user=request.user,
                                                    recipe=recipe).first()
        serializer = ShoppingCartSerializer(recipe, data=request.data,
                                            context={'request': request})
        if request.method == 'DELETE' and shopping_cart:
            shopping_cart.delete()
            return Response({'message': 'Рецепт успешно удален из корзины'},
                            status=status.HTTP_204_NO_CONTENT)
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Выгружаем список продуктов из корзины (формат txt)."""
        ingredients = RecipeIngredients.objects.filter(
            recipe__shopping_cart__user=request.user).values(
                'ingredient__name',
                'ingredient__measurement_unit',
                'amount').order_by('ingredient__name')
        shopping_list = self.create_ingredient_list(ingredients)
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format('Список_покупок.txt')
        )
        return response

    def create_ingredient_list(self, queryset) -> list:
        """Доп.функция: создаем список продуктов по рецептам из корзины."""
        ingredient_data = defaultdict(int)
        for ingredient in queryset:
            ingredient_name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount']
            key = f'{ingredient_name} ({measurement_unit})'
            ingredient_data[key] += amount

        ingredient_list = []
        ingredient_list.append('Список продуктов: \n')
        for ingredient, amount in ingredient_data.items():
            ingredient_list.append(f'{ingredient} - {amount} \n')

        return ingredient_list
