from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


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

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class UserStatisticViewSet(viewsets.GenericViewSet,
                           viewsets.mixins.ListModelMixin):

    queryset = User.objects.all()
    serializer_class = StatisticSerializer

    def get_queryset(self):
        return Statistic.objects.filter(user=self.request.user)
