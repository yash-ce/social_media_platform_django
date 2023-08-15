from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer, AllPostSerializer

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User registered successfully'})

class AuthenticateUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)})

class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')

        if not title or not description:
            return Response({'error': 'Please provide both title and description'}, status=400)

        post = Post.objects.create(title=title, description=description, user=request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data)

class PostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
            post.delete()
            return Response({'message': 'Post deleted successfully'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.likes.add(request.user)
            return Response({'message': 'Post liked successfully'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.likes.remove(request.user)
            return Response({'message': 'Post unliked successfully'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            comment_text = request.data.get('comment')
            comment = Comment.objects.create(text=comment_text, user=request.user, post=post)
            serializer = CommentSerializer(comment)
            return Response( {'comment id' : serializer.data["id"]})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)


class GetAllPostsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(user=request.user).order_by('-created_at')
        serializer = AllPostSerializer(posts, many=True)
        return Response(serializer.data)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            request.user.following.add(user_to_follow)
            return Response({'message': 'User followed successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            request.user.following.remove(user_to_unfollow)
            return Response({'message': 'User unfollowed successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

