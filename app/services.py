from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Like, Dislike, Statistic

User = get_user_model()


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)

    profile = Statistic.objects.get_or_create(user=user)[0]
    profile.total_likes += 1
    profile.save(update_fields=('total_likes',))

    if is_disliked(obj, user):
        remove_dislike(obj, user)

    return like


def remove_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)

    profile = Statistic.objects.get_or_create(user=user)[0]
    profile.total_likes -= 1
    profile.save(update_fields=('total_likes',))

    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def add_dislike(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    dislike = Dislike.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)

    profile = Statistic.objects.get_or_create(user=user)[0]
    profile.total_dislikes += 1
    profile.save(update_fields=('total_dislikes',))

    if is_liked(obj, user):
        remove_like(obj, user)

    return dislike


def remove_dislike(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)

    profile = Statistic.objects.get_or_create(user=user)[0]
    profile.total_dislikes -= 1
    profile.save(update_fields=('total_dislikes',))

    Dislike.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_liked(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    like = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)

    return like.exists()


def is_disliked(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    dislike = Dislike.objects.filter(content_type=obj_type, object_id=obj.id, user=user)

    return dislike.exists()
