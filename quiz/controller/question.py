from django.http import HttpResponse, JsonResponse
from quiz.models.Level import Level
from quiz.models.Player import Player
from quiz.models.Question import Question
import datetime, json

def getQuestion(request):
    email = request.GET.get('email') 
    try:
        user = Player.objects.get(email=email)
    except:
        user = Player.objects.create(email=email)
    score = user.score         
    q_num = (score/10) + 1;
    response = []
    question = Question.objects.get(id=q_num)
    img_url = request.build_absolute_uri(question.image.url)
    audio_url = request.build_absolute_uri(question.audio.url)
    return JsonResponse ({
        'question':question.question_text,
        'hint':question.answer_text,
        'score':score,
        'image':img_url,
        'audio':audio_url,
    })

def checkAnswer(request):
    email = request.GET.get('email')
    user = Player.objects.get(email=email)
    score = user.score
    q_num = (score/10) + 1;
    question = Question.objects.get(id=q_num)
    answer = request.GET.get('answer')
    if question.answer_text == answer:
        user.score = user.score + 10
        user.submit_time = datetime.datetime.now()
        user.save()
        return JsonResponse({
            'isTrue': 1
    })
    else:
        return JsonResponse({
            'isTrue': 0
    })

def leaderboard(request):
    p = Player.objects.order_by('-score','submit_time')
    current_rank = 1
    players_array = []
    for player in p:
        player.rank = current_rank
        players_array.append({
            'name':player.name,
            'rank':player.rank,
            'email':'',
            'score':player.score,
        })
        current_rank += 1

    return JsonResponse(players_array,safe=False)

