import json
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse

from django.views import View

from postings.models import Posting
from users.models import User

class PostingView(View):
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

    def get(self, request):
        postings = Posting.objects.all()
        result = []
        for posting in postings:
            result.append({
                'image'        : posting.image_url,
                'content'      : posting.content,
                'created_at'   : posting.created_at,
                'like'         : posting.number_of_likes,
                'username'     : posting.user.username,
                'profile_photo': posting.user.profile_photo,
                'user_id'      : posting.user_id
            })

        return JsonResponse({'result':result}, status=200)
