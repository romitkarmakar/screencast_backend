from django.http import HttpResponse, JsonResponse
from quiz.models.Level import Level
from quiz.models.Player import Player
from quiz.models.Question import Question
import datetime
import json
from quiz.controller.authentication import verifyUser
from django.utils import timezone
import urllib

def currentLevel():
    now = timezone.now()
    levels = Level.objects.all()
    for level in levels:
        if now >= level.start_time and now <= level.end_time:
            print(level.level_number)
            return level.level_number


def nextLevel():
    now = timezone.now()
    levels = Level.objects.all()
    for level in levels:
        if now >= level.end_time:
            continue
        if now <= level.start_time:
            value = str(level.start_time - now)
            valueArr = value.split(".")
            valueArr1 = valueArr[0].split(":")
            return ["{} hour and {} minutes".format(valueArr1[0], valueArr1[1]), level.level_number]


def getLevel(request):
    if currentLevel():
        return JsonResponse({"status": 200, "level": currentLevel()})
    else:
        return JsonResponse({"status": 400, "level": nextLevel()[1], "message": nextLevel()[0]})


def getQuestion(request):
    currLevel = currentLevel()
    question = {}
    email = request.GET.get("email")
    if verifyUser(email):
        user = Player.objects.get(email=email)
        score_array = user.score.split(",")
        if currLevel is not None:
            score = int(score_array[currLevel - 1])

        else:
            return JsonResponse({
                    "status": 500,
                    "message": "No questions"
                })

        q_num = int((score / 10))
        print(q_num)
        level = Level.objects.get(level_number=currLevel)
        questions = Question.objects.filter(level=level).order_by("pk")
        print(questions)

        for index, q in enumerate(questions):
            print(index)
            if q_num == index:
                question = questions[index]
                img_url = request.build_absolute_uri(question.image.url)
                audio_url = request.build_absolute_uri(question.audio.url)
                return JsonResponse(
                    {
                        "status": 200,
                        "question": question.question_text,
                        "hint": question.hint,
                        "score": score,
                        "image": img_url,
                        "audio": audio_url,
                    }
                )
        return JsonResponse({
                    "status": 500,
                    "message": "No questions"
                })

    else:
        return JsonResponse({"status": 404, "message": "User Not Registered"})


def checkAnswer(request):
    currLevel = currentLevel()
    email = request.GET.get("email")
    user = Player.objects.get(email=email)
    score_array = user.score.split(",")
    print(score_array)
    score = int(score_array[currentLevel() - 1])
    q_num = int((score / 10))
    level = Level.objects.get(level_number=currLevel)
    questions = Question.objects.filter(level=level).order_by("pk")
    for index, q in enumerate(questions):
        if q_num == index:
            question = questions[index]
            answer = request.GET.get("answer")
            print(answer)
            answer = urllib.parse.unquote(answer)
            answer = answer.lower()
            answer = answer.strip()
            if question.checkAnswer(answer):
                score_array[currLevel - 1] = str(int(score_array[currLevel - 1]) + 10)
                user.submit_time = timezone.now()
                user.score = ",".join(score_array)
                user.total_score += 10
                user.save()
                return JsonResponse({"isTrue": 1})
            else:
                return JsonResponse({"isTrue": 0})


def leaderboard(request):
    p = Player.objects.order_by("-total_score", "submit_time")
    current_rank = 1
    players_array = []
    for player in p:
        player.rank = current_rank
        players_array.append(
            {
                "name": player.name,
                "rank": player.rank,
                "score": player.total_score,
                "image": player.image,
            }
        )
        current_rank += 1
    return JsonResponse(players_array, safe=False)
