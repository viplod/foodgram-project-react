from django.db import models
from users.models import User

SLICE_REVIEW = 30


class Tag(models.Model):
    """Модель для работы с тегами"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега в HEX'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Slug тега',
    )

    def __str__(self):
        return self.name[:SLICE_REVIEW]

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


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
        return self.name[:SLICE_REVIEW]


class Recipe(models.Model):
    """Модель для работы с рецептами"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField('Описание', blank=True, null=True)
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
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
        ordering = ('name',)
        ordering = ('-date_pub',)

    def __str__(self):
        return self.name[:SLICE_REVIEW]


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

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


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
