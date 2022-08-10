from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Абстрактная модель пользователя."""
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    email = models.EmailField(verbose_name='email пользователя',
                              unique=True,
                              error_messages={
                                  'unique': "Пользователь с таким email уже существует.",
                              },
                              )
    username = models.CharField(
        verbose_name='имя пользователя',
        max_length=150,
        unique=True,
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
        },
    )


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
