from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Sum
from .models import Recipe, Favorite, ShoppingCart, RecipeIngredient
from .serializers import RecipeSerializer, RecipeShortSerializer
# from core.models import Tag, Ingredient
from django_filters.rest_framework import DjangoFilterBackend


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_carts__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))
        content = 'Список покупок:\n\n'
        for item in ingredients:
            content += (
                f"{item['ingredient__name']} - "
                f"{item['total_amount']} "
                f"{item['ingredient__measurement_unit']}\n"
            )
        response = HttpResponse(
            content_type='text/plain',
            headers={
                'Content-Disposition': 'attachment;'
                'filename="shopping_list.txt"'
            },
        )
        response.write(content)
        return response
