from django.urls import path

from .views import (
    AuthView, UserSelfView, UserView
)

urlpatterns = [
    path('signup', UserView.as_view()),
    path('signin', AuthView.as_view()),
    path('me', UserSelfView.as_view()),
    path('signout', AuthView.as_view()),
    path('all', UserView.as_view())
]
