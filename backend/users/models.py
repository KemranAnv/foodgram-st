from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This model can be used to add additional fields or methods in the future.
    """
    email = models.EmailField(
        'Электронная почта',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                'Недопустимые символы в имени пользователя.',
            )
        ],
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='avatars/',
        blank=True,
        null=True,
        default='avatars/default_avatar.png',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    Model to represent a subscription to a user.
    This can be used to track which users are subscribed to which other users.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_subscription',
            ),
        ]

    def __str__(self):
        return (
            f'{self.user.username} подписан на '
            f'{self.subscribed_to.username}'
        )
