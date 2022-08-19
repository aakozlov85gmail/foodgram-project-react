import csv

from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from recipes.models import (
    Tag,
                            Ingredient,
                            Recipe,
                            IngredientRecipe,
                            ShoppingCart,
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeCreateModifySerializer,
)
from .filters import IngredientFilter, RecipeFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeCreateModifySerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        current_user = self.request.user
        if current_user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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

        @action(detail=False, methods=['POST','DELETE'])
        def shopping_cart(self, request, recipe_id):
            current_user = self.request.user
            if current_user.is_anonymous:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            recipe = get_object_or_404(Recipe, id=recipe_id)

            if self.request.method=='POST':
                ShoppingCart.





