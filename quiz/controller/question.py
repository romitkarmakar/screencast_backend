from django.http import HttpResponse, JsonResponse
from quiz.models.Level import Level
from quiz.models.Player import Player
from quiz.models.Question import Question

def getQuestion(request):
    email = request.GET.get('email') 
    user = Player.objects.get(email=email)
    q_num = request.GET.get('q_number')
    response = []
    question = Question.objects.get(id=q_num)
    return JsonResponse ({
        'question':question.question_text,
        'hint':question.answer_text,
    })

def checkAnswer(request):
    q_num = request.GET.get('q_number')
    question = Question.objects.get(id=q_num)
    answer = request.GET.get('answer')
    if question.answer_text == answer:
        return JsonResponse({
            'isTrue': 1
    })
    else:
        return JsonResponse({
            'isTrue': 0
    })
