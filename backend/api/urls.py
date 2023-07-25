from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ChangePasswordView, CurrentUserMeView, CustomUserViewSet,
                    FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingCartViewSet, SubscriptionsViewSet, TagViewSet)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('users/me/', CurrentUserMeView.as_view()),
    path('users/set_password/', ChangePasswordView.as_view()),
    path('users/subscriptions/', SubscriptionsViewSet.as_view(
        {'get': 'subscriptions'})),
    path('users/<int:pk>/subscribe/', SubscriptionsViewSet.as_view(
        {'post': 'subscribe', 'delete': 'subscribe'})),
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
        {'post': 'favorite', 'delete': 'favorite'})),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view(
        {'post': 'shopping_cart', 'delete': 'shopping_cart'})),
    path('recipes/download_shopping_cart/', ShoppingCartViewSet.as_view(
        {'get': 'download_shopping_cart'})),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
