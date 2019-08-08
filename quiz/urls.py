from django.urls import path
from .controller import question

urlpatterns = [
    path('getQuestion', question.getQuestion, name='getQuestion'),
    path('checkAnswer', question.checkAnswer, name='checkAnswer'),
]
