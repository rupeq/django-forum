from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import *
from .models import Post, Comment, Statistic
from .mixins import LikeDislikeMixin


class UserView(viewsets.GenericViewSet,
               viewsets.mixins.CreateModelMixin,
               viewsets.mixins.ListModelMixin,
               viewsets.mixins.RetrieveModelMixin,
               viewsets.mixins.UpdateModelMixin):

    queryset = User.objects.all()

    default_serializer_class = UserSerializer

    serializer_classes_by_action = {
        "list": ListUserSerializer,
        "create": UserSerializer,
        "retrieve": UserSerializer,
        "update": UpdateUserSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class PostViewSet(viewsets.GenericViewSet,
                  viewsets.mixins.CreateModelMixin,
                  viewsets.mixins.ListModelMixin,
                  viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.UpdateModelMixin,
                  LikeDislikeMixin):

    queryset = Post.objects.all()

    default_serializer_class = ListPostSerializer

    serializer_classes_by_action = {
        "list": ListPostSerializer,
        "create": PostSerializer,
        "retrieve": PostSerializer,
        "update": PostSerializer,
    }

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return Post.objects.filter(status=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)


class CommentViewSet(viewsets.GenericViewSet,
                  viewsets.mixins.CreateModelMixin,
                  viewsets.mixins.ListModelMixin,
                  viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.UpdateModelMixin):

    queryset = Comment.objects.all()

    default_serializer_class = ListCommentSerializer

    serializer_classes_by_action = {
        "list": ListCommentSerializer,
        "create": CommentSerializer,
        "retrieve": CommentSerializer,
        "update": CommentSerializer,
    }

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)


class UserStatisticViewSet(viewsets.GenericViewSet,
                           viewsets.mixins.ListModelMixin):

    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer

    def get_queryset(self):
        return Statistic.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        user = self.request.user

        profile = Statistic.objects.get_or_create(user=user)[0]

        posts_likes = 0
        posts_dislikes = 0

        for i in Post.objects.filter(author=user):
            posts_likes += i.likes_count
            posts_dislikes += i.dislikes_count

        profile.total_self_posts_likes = posts_likes
        profile.total_self_posts_dislikes = posts_dislikes
        profile.save()

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
