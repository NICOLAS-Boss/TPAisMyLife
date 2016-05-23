from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
