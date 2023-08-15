from django.urls import path
from . import views

urlpatterns = [
    path('api/register', views.RegisterUserView.as_view()),
    path('api/authenticate', views.AuthenticateUserView.as_view()),
    path('api/user', views.UserProfileView.as_view()),
    path('api/posts', views.CreatePostView.as_view()),
    path('api/posts/<int:post_id>', views.PostView.as_view()),
    path('api/like/<int:post_id>', views.LikePostView.as_view()),
    path('api/unlike/<int:post_id>', views.UnlikePostView.as_view()),
    path('api/comment/<int:post_id>', views.AddCommentView.as_view()),
    path('api/all_posts', views.GetAllPostsView.as_view()),
    path('api/follow/<int:user_id>', views.FollowUserView.as_view()),
    path('api/unfollow/<int:user_id>', views.UnfollowUserView.as_view()),
]