import json
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse

from django.views import View

from postings.models import Like, Posting, Comment
from users.decorators import login_required

class PostingView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)

            content   = data['content']
            image_url = data['image_url']

            Posting.objects.create(
                user_id   = request.user.id,
                content   = content,
                image_url = image_url
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_required
    def get(self, request):
        last_id = request.GET.get('last_id')

        query = Posting.objects.order_by('-id')
        if last_id:
            try:
                last_id = int(last_id)
            except ValueError:
                return JsonResponse({'message':'INVALID_QUERY_PARAM'}, status=400)
            query = query.filter(id__lt=last_id)
        postings = query[:10]

        result = [
            {
                'image'        : posting.image_url,
                'content'      : posting.content,
                'created_at'   : posting.created_at,
                'like'         : posting.number_of_likes,
                'username'     : posting.user.username,
                'profile_photo': posting.user.profile_photo,
                'user_id'      : posting.user_id,
                'id'           : posting.id
            }
            for posting in postings
        ]

        return JsonResponse({'result':result}, status=200)

class CommentView(View):
    @login_required
    def post(self, request, posting_id):
        data = json.loads(request.body)

        content = data['content']

        comment = Comment.objects.create(
            content = content,
            user_id = request.user.id,
            posting_id = posting_id
        )

        result = self.to_json(comment)

        return JsonResponse({"result":result}, status=201)

    @login_required
    def get(self, request, posting_id):
        comments = Comment.objects.filter(posting_id=posting_id).order_by('id')

        result = [
            self.to_json(comment)
            for comment in comments
        ]

        return JsonResponse({'result':result}, status=200)

    def to_json(self, comment):
        return {
            'content'      : comment.content,
            'created_at'   : comment.created_at,
            'id'           : comment.id,
            'username'     : comment.user.username,
            'profile_photo': comment.user.profile_photo,
            'user_id'      : comment.user_id,
            'posting_id'   : comment.posting_id
        }

class LikeView(View):
    @login_required
    def post(self, request, posting_id):
        if not Like.objects.filter(
            user_id=request.user.id,
            posting_id=posting_id,
        ).exists():
            Like.objects.create(
                user_id = request.user.id,
                posting_id = posting_id
            )
        return JsonResponse({'message':'SUCCESS'}, status=200)


class LikersView(View):
    @login_required
    def get(self, request, posting_id):
        likers = Like.objects.filter(posting_id=posting_id)
        result = [
            {
                'username'     : liker.user.username,
                'profile_photo': liker.user.profile_photo,
                'user_id'      : liker.user_id,
                'posting_id'   : liker.posting_id
            }
            for liker in likers
        ]
        return JsonResponse({"result":result}, status=200)
