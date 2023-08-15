from rest_framework import serializers 
from user_app.models import * 
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    def get_followers(self, obj):
        return obj.followers.count()

    def get_followings(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'followers', 'followings']

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return obj.comments.count()

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'comments', 'likes']

class AllPostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_comments(self, obj):
        all_comments = obj.comments.all()
        comments_list = []
        for comment in all_comments:
            d = {
                'id' : comment.id,
                'comment' : comment.text 
            }
            comments_list.append(d)
        return comments_list

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'comments', 'likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user']
