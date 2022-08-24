from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import User, Subscription
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    ShoppingCart,
    IngredientRecipe,
)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeGetSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer()
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='ingredientrecipe_set',
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=current_user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=current_user,
            recipe=obj
        ).exists()


class RecipeCreateModifySerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = IngredientRecipeSerializer(many=True,)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients':
                'Необходимо добавить хотя бы 1 игредиент'
            })
        for ingredient_item in ingredients:
            if ingredients.count(ingredient_item) > 1:
                raise serializers.ValidationError({
                    'ingredients':
                    'Ингридиенты должны быть уникальными!'
                })

            amount = ingredient_item.get('amount')
            if float(amount) <= 0:
                raise serializers.ValidationError({
                    'amount':
                    'Проверьте, что количество ингредиента больше нуля!'
                })

        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать хотя бы один тэг!'
            })
        for tag in tags:
            if tags.count(tag) > 1:
                raise serializers.ValidationError({
                    'tags': 'Тэги должны быть уникальными!'
                })

        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовление должно быть больше нуля!'
            })
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def ingredients_creation(self, ingredients, recipe):
        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(
                           ingredient=get_object_or_404(
                               Ingredient,
                               id=ingredient_item.get('id')
                           ),
                           recipe=recipe,
                           amount=ingredient_item.get('amount')
            ) for ingredient_item in ingredients]
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.ingredients_creation(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(tags_data)
        self.ingredients_creation(ingredients_data, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(
            instance, context=context).data


class ShoppingCartValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )
        read_only_fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = self.context.get('recipe')
        recipe_in_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe)
        if request.method == 'POST':
            if recipe_in_cart.exists():
                raise serializers.ValidationError({
                    'errors': 'Этот рецепт уже добавлен в корзину покупок!'
                })
        if request.method == 'DELETE' and not recipe_in_cart.exists():
            raise serializers.ValidationError({
                'errors': 'Этого рецепта нет в корзине покупок пользователя!'
            })
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class FavoriteValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe',
        )
        read_only_fields = (
            'user',
            'recipe',
        )

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        recipe = self.context.get('recipe')
        recipe_in_favorite = Favorite.objects.filter(
            user=user, recipe=recipe)
        if request.method == 'POST':
            if recipe_in_favorite.exists():
                raise serializers.ValidationError({
                    'errors': 'Этот рецепт уже есть в избранном!'
                })
        if request.method == 'DELETE' and not recipe_in_favorite.exists():
            raise serializers.ValidationError({
                'errors': 'Этого рецепта нет в избранном пользователя!'
            })
        return data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit is not None:
            recipes = obj.recipes.all()[:int(limit)]
        return SubscriptionRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'author')
        read_only_fields = ('user', 'author')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        author = self.context.get('author')
        subscription = Subscription.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if subscription.exists():
                raise serializers.ValidationError({
                    'errors': 'Такая подписка уже оформлена!'
                })
            elif user == author:
                raise serializers.ValidationError({
                    'errors': 'Вы не можете подписаться на самого себя!'
                })
        if request.method == 'DELETE' and not subscription.exists():
            raise serializers.ValidationError({
                'errors': 'Такой подписки не существует!'
            })
        return data
