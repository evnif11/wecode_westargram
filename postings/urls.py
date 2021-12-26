from django.urls import path

from postings.views import CommentView, LikeView, LikersView, PostingView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<int:posting_id>/comments', CommentView.as_view()),
    path('/<int:posting_id>/like', LikeView.as_view()),
    path('/<int:posting_id>/likers', LikersView.as_view()),
]
