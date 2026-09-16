from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Просмотр постов и управление собственными публикациями."""

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр списка групп и отдельной группы."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и изменение комментариев к указанному в URL посту."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self) -> Post:
        """Возвращает родительский пост или вызывает ошибку 404."""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self) -> QuerySet[Comment]:
        return self.get_post().comments.select_related('author')

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(author=self.request.user, post=self.get_post())
