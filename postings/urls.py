from django.urls import path

from postings.views import CommentView, FollowView, FollowerListView, FollowingListView, LikeView, LikersView, PostingView, UnfollowView

urlpatterns = [
    path('postings', PostingView.as_view()),
    path('postings/<int:posting_id>/comments', CommentView.as_view()),
    path('postings/<int:posting_id>/like', LikeView.as_view()),
    path('postings/<int:posting_id>/likers', LikersView.as_view()),
    path('follow', FollowView.as_view()),
    path('unfollow', UnfollowView.as_view()),
    path('users/<int:user_id>/follower', FollowerListView.as_view()),
    path('users/<int:user_id>/following', FollowingListView.as_view()),
]
