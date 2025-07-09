from django.urls import path
from .views import FlashcardFormAPIView,FlashcardReviewAPIView,FlashcardHTMLView
from .views import register_user,login_user

urlpatterns=[
    path('api/register/',register_user,name='register-user'),
    path('api/login/',login_user,name='login-page'),
    path('api/flashcards/',FlashcardFormAPIView.as_view(),name='add_flashcard'),
    path('api/flashcards/<int:pk>/',FlashcardReviewAPIView.as_view(),name='review_flashcards'),
    path('api/home/',FlashcardHTMLView.as_view(),name='flashcard-html'),
]