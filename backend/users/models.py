from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Абстрактная модель пользователя."""

    pass


class Subscription(models.Model):
    """Модель подписки пользователя."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribtion',
            ),
        ]
