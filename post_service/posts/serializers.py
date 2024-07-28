from rest_framework import serializers
from .models import Discussion, Comment, Hashtag
from django.contrib.auth import get_user_model

User = get_user_model()

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']

class DiscussionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    hashtags = HashtagSerializer(many=True, read_only=True)
    view_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'user', 'text', 'image', 'hashtags', 'created_on', 'view_count']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'discussion', 'text', 'created_on', 'likes']