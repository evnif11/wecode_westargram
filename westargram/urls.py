from django.urls import path, include

urlpatterns = [
    path('', include('postings.urls')),
    path('users', include('users.urls')),
]
