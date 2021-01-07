from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Post, Comment, Statistic
from .services import is_liked, is_disliked

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_obj = User(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ListPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'create', 'theme', 'sphere', 'text', 'likes_count', 'dislikes_count')

    def is_liked(self, obj):
        user = self.request.user
        return is_liked(user, obj)

    def is_disliked(self, obj):
        user = self.request.user
        return is_disliked(user, obj)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('theme', 'sphere', 'text')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        profile = Statistic.objects.get_or_create(user=user)[0]
        profile.total_posts += 1
        profile.save()

        post = Post.objects.create(**validated_data)
        post.save()

        return validated_data


class ListCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('author', 'create', 'post', 'text', 'parent')

    def is_liked(self, obj):
        user = self.request.user
        return is_liked(user, obj)

    def is_disliked(self, obj):
        user = self.request.user
        return is_disliked(user, obj)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('post', 'text', 'parent')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        profile = Statistic.objects.get_or_create(user=user)[0]
        profile.total_comments += 1
        profile.save()

        return validated_data


class StatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statistic
        fields = ('total_posts', 'total_comments',
                  'total_posts_likes', 'total_posts_dislikes',
                  'total_self_posts_likes', 'total_self_posts_dislikes')
