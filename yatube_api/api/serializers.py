import base64

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import IntegrityError
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = PrimaryKeyRelatedField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('pub_date',)

    def create(self, validated_data):
        if 'group' not in self.initial_data:
            return Post.objects.create(**validated_data)
        group_id = self.initial_data.get('group')
        group = Group.objects.get(pk=group_id)
        return Post.objects.create(**validated_data, group=group)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        if 'group' in self.initial_data:
            group = Group.objects.get(pk=self.initial_data.get('group'))
            instance.group = group
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('created', 'post')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def create(self, validated_data):
        user_to_follow_str = self.initial_data.get('following')
        try:
            user_to_follow = User.objects.get(username=user_to_follow_str)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Пользователь, на которого вы хотите'
                'подписаться, не существует!')
        user = validated_data.get('user')
        if user == user_to_follow:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        try:
            follow = Follow.objects.create(user=user, following=user_to_follow)
        except IntegrityError:
            raise serializers.ValidationError('Нельзя повторно подписаться!')
        return follow
