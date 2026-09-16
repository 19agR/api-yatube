from django.contrib.auth import get_user_model
from django.db import models

GROUP_TITLE_MAX_LENGTH = 200
MODEL_REPR_MAX_LENGTH = 30

User = get_user_model()


class Group(models.Model):
    """Тематическая группа публикаций."""

    title = models.CharField(max_length=GROUP_TITLE_MAX_LENGTH)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title[:MODEL_REPR_MAX_LENGTH]


class Post(models.Model):
    """Публикация пользователя с необязательными группой и изображением."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self) -> str:
        return self.text[:MODEL_REPR_MAX_LENGTH]


class Comment(models.Model):
    """Комментарий пользователя к публикации."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
