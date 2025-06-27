from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64
from .models import Recipe, RecipeIngredient, Favorite, ShoppingCart
from core.serializers import TagSerializer
from users.serializers import UserSerializer
from api.serializers import RecipeShortSerializer

User = get_user_model()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.CharField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def validate_image(self, value):
        try:
            header, data = value.split(';base64,')
            decoded_file = base64.b64decode(data)
            return ContentFile(decoded_file, name='recipe_image.jpg')
        except ValueError:
            raise serializers.ValidationError(
                'Неверный формат изображения (ожидается base64).'
            )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Необходимо указать хотя бы один ингредиент.'}
            )
        ingredient_ids = [item['id'] for item in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты не должны повторяться.'}
            )
        for item in ingredients:
            if item['amount'] < 1:
                raise serializers.ValidationError(
                    {'amount': 'Количество должно быть больше 0.'}
                )
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = self.initial_data.get('tags')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags_data)
        for item in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=item['ingredient']['id'],
                amount=item['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        instance.recipe_ingredients.all().delete()
        for item in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=item['ingredient']['id'],
                amount=item['amount']
            )
        instance.image = validated_data.pop('image')
        return super().update(instance, validated_data)
