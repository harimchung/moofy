from .models import Movie, Comment
# from accounts.models import User
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        # 'nickname'
        fields = ( 'id', 'movie', 'content', 'user', 'rating', 'nickname')
    


class MovieSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comment_set.count", read_only=True)
    class Meta:
        model = Movie
        fields = "__all__"
