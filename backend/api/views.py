import csv

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    ShoppingCart,
    Favorite,
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateModifySerializer,
    ShoppingCartSerializer,
    FavoriteSerializer,
    CustomUserSerializer,
    SubscriptionSerializer,
)
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorAdminOrReadOnly
from users.models import User, Subscription


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        current_user = self.request.user
        author = get_object_or_404(User, pk=id)
        subscription = Subscription.objects.filter(
            user=current_user,
            author=author
        )
        if request.method == 'POST':
            if subscription.exists():
                data = {
                    'errors':
                        'Подписка на автора уже оформлена.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            elif current_user == author:
                data = {
                    'errors':
                        'Вы не можете подписаться на самого себя.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(user=current_user, author=author)
            serializer = SubscriptionSerializer(
                author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subscription.exists():
                data = {
                    'errors':
                        'Такой подписки не существует.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAuthorAdminOrReadOnly,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeCreateModifySerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount')).values_list(
            'ingredient__name', 'ingredient_amount',
            'ingredient__measurement_unit',
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shoppingcart.csv"')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        for item in list(ingredients):
            writer.writerow(item)
        return response

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        current_user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_cart = ShoppingCart.objects.filter(
            user=current_user, recipe=recipe)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(recipe)
            if recipe_in_cart.exists():
                data = {
                    'errors':
                    'Этот рецепт уже добавлен в корзину покупок.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=current_user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not recipe_in_cart.exists():
                data = {
                    'errors':
                    'Этого рецепта нет в корзине покупок пользователя.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            recipe_in_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        current_user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_favorite = Favorite.objects.filter(
            user=current_user, recipe=recipe)
        if request.method == 'POST':
            serializer = FavoriteSerializer(recipe)
            if recipe_in_favorite.exists():
                data = {
                    'errors':
                    'Этот рецепт уже есть в избранном.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=current_user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not recipe_in_favorite.exists():
                data = {
                    'errors':
                    'Этого рецепта нет в избранном пользователя.'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            recipe_in_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
