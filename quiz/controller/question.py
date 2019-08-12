from django.http import HttpResponse, JsonResponse
from quiz.models.Level import Level
from quiz.models.Player import Player
from quiz.models.Question import Question
import datetime, json
from quiz.controller.authentication import verifyUser
from django.utils import timezone
  
def currentLevel():
    now = timezone.now()
    levels = Level.objects.all()
    for level in levels:
        if now >= level.start_time and now <= level.end_time:
            print(level.level_number)
            return level.level_number


def getQuestion(request):
    email = request.GET.get('email') 
    if verifyUser(email):
        user = Player.objects.get(email=email)
        score_array = user.score.split(",")
        score = int(score_array[currentLevel()])       
        q_num = (score/10) + 1

        level = Level.objects.get(level_number=currentLevel())
        questions = Question.objects.filter(level=level)
        question = [q for q, index in enumerate(questions) if index == q_num]

        img_url = request.build_absolute_uri(question.image.url)
        audio_url = request.build_absolute_uri(question.audio.url)
        return JsonResponse ({
            'question':question.question_text,
            'hint':question.answer_text,
            'score':score,
            'image':img_url,
            'audio':audio_url,
        })
    else:
        return JsonResponse({
            'status':404,
            'message':"User Not Registered"
    })    

def checkAnswer(request):
    email = request.GET.get('email')
    user = Player.objects.get(email=email)
    score_array = user.score.split(",")
    score = int(score_array[currentLevel()])        
    q_num = (score/10) + 1
    level = Level.objects.get(level_number=currentLevel())
    questions = Question.objects.filter(level=level)
    question = [q for q, index in enumerate(questions) if index == q_num ]

    answer = request.GET.get('answer')
    answer.lower()
    answer.strip()
    if question.answer_text == answer:
        score_array[currentLevel()] = str(int(score_array[currentLevel()])+10)
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
        score = 0
        for index in player.score:
            score+=int(index)
        players_array.append({
            'name':player.name,
            'rank':player.rank,
            'score':score,
            'image':player.image,
        })
        current_rank += 1
    return JsonResponse(players_array,safe=False)

