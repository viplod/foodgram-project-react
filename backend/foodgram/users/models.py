from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомизированная модель для работы с пользователями"""
    username = models.CharField(
        max_length=150
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'username', 'last_name', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return str(self.username)


class Follow(models.Model):
    """Модель для работы с подписками на авторов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='user_author'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан {self.author}'
