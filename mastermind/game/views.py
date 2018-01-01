from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
import json
from .models import *


def index(request):
    return render(request, "game/index.html")


def game_view(request, id):
    game = Game.objects.filter(game_id=id)
    if len(game) != 1:
        out = {
            "status": "error",
            "error": "not-found"
        }
        resp = HttpResponse(json.dumps(out))
        resp.status_code = 404
        return resp
    game = game[0]
    out = {
        "status": "success",
        "game_id": game.game_id,
        "start_time": game.start_time.timestamp()
    }
    return HttpResponse(json.dumps(out))


def game_create_view(request):
    if request.method == "POST":
        game = Game(code_colour_1=request.POST['pos1'], code_colour_2=request.POST['pos2'],
                    code_colour_3=request.POST['pos3'], code_colour_4=request.POST['pos4'])
        game.save()
        out = {
            "status": "success",
            "game_id": game.game_id,
            "start_time": game.start_time.timestamp()
        }
        return HttpResponse(json.dumps(out))
    else:
        raise HttpResponseNotAllowed(permitted_methods=['POST'])


def game_guesses_view(request, id):
    game = Game.objects.filter(game_id=id)
    if len(game) != 1:
        out = {
            "status": "error",
            "error": "not-found"
        }
        resp = HttpResponse(json.dumps(out))
        resp.status_code = 404
        return resp
    game = game[0]
    guesses = GameRow.objects.filter(game=game).order_by('time')
    out = {
        "status": "success",
        "guesses-left": game.guesses_left,
        "finished": game.game_finished,
        "guesses": [],
    }
    for guess in guesses:
        out["guesses"].append({
            "time": guess.time.timestamp(),
            "pos1": guess.guess_colour_1,
            "pos2": guess.guess_colour_2,
            "pos3": guess.guess_colour_3,
            "pos4": guess.guess_colour_4,
            "num_black": guess.num_black_pegs,
            "num_white": guess.num_white_pegs,
            "correct": guess.guess_correct,
        })
    return HttpResponse(json.dumps(out))


def game_guess_view(request, id):
    if request.method == "POST":
        game = Game.objects.filter(game_id=id)
        if len(game) != 1:
            out = {
                "status": "error",
                "error": "not-found"
            }
            resp = HttpResponse(json.dumps(out))
            resp.status_code = 404
            return resp
        game = game[0]
        if not game.game_finished:
            row = GameRow(game=game, guess_colour_1=request.POST['pos1'], guess_colour_2=request.POST['pos2'],
                          guess_colour_3=request.POST['pos3'], guess_colour_4=request.POST['pos4'])
            row.save()
            out = {
                "status": "success",
                "correct": row.guess_correct,
                "last": game.game_finished
            }
            return HttpResponse(json.dumps(out))
        else:
            out = {
                "status": "error",
                "error": "game-finished"
            }
            resp = HttpResponse(json.dumps(out))
            resp.status_code = 410
    else:
        raise HttpResponseNotAllowed(permitted_methods=['POST'])
