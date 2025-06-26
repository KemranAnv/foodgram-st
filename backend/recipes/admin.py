from django.contrib import admin
from .models import Recipe, RecipeIngredient, Favorite, ShoppingCart


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date', 'cooking_time')
    search_fields = ('name', 'author__email')
    list_filter = ('tags', 'pub_date')
    # filter_horizontal = ('ingredients', 'tags')
    inlines = (RecipeIngredientsInline,)
    filter_horizontal = ('tags',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__email', 'recipe__name')
    empty_value_display = '-пусто-'
