from rest_framework.decorators import action
from rest_framework.response import Response

from .services import add_like, add_dislike, remove_like, remove_dislike, is_liked, is_disliked


class LikeDislikeMixin:

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        obj = self.get_object()
        add_like(obj, request.user)

        return Response()

    @action(methods=['POST'], detail=True)
    def unlike(self, request, pk=None):
        obj = self.get_object()
        remove_like(obj, request.user)

        return Response()

    @action(methods=['POST'], detail=True)
    def dislike(self, request, pk=None):
        obj = self.get_object()
        add_dislike(obj, request.user)

        return Response()

    @action(methods=['POST'], detail=True)
    def undislike(self, request, pk=None):
        obj = self.get_object()
        remove_dislike(obj, request.user)

        return Response()
