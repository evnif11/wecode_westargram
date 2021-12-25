from django.urls import path

from postings.views import CommentView, PostingView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/<int:posting_id>/comments', CommentView.as_view()),
]
