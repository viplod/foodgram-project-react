from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

from users.models import User


class Tag(models.Model):
    """Модель для работы с тегами"""
    name = models.CharField(
        max_length=50,   # В redoc - string <= 200 characters
        verbose_name='Название тега',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега в HEX',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,   # В redoc - string <= 200 characters
        verbose_name='Slug тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.SLICE_REVIEW]


class Ingredient(models.Model):
    """Модель для работы с ингредиентами"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.SLICE_REVIEW]


class Recipe(models.Model):
    """Модель для работы с рецептами"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField('Описание')
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1,
            'Время приготовления должно быть больше 1 минуты')
            ]
        )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги'
    )

    date_pub = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date_pub',)

    def __str__(self):
        return self.name[:settings.SLICE_REVIEW]


class TagRecipe(models.Model):
    """Вспомогательная таблица для модели Recipe, поле тег"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class IngredientInRecipe(models.Model):
    """Вспомогательна таблица для модели Recipe, поле amount"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class FavoriteRecipe(models.Model):
    """Вспомогательная модель для модели Recipe, поле is_favorite"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe_favorite'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - {self.user}'


class ShoppingRecipe(models.Model):
    """Вспомогательная модель для модели Recipe, поле is_in_shopping_cart"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списках покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe_shopping'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - {self.user}'
