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
            row = GameRow(game=game, guess_colour_1=request.POST['pos1'], guess_colour_2=request.POST['pos2'],
                          guess_colour_3=request.POST['pos3'], guess_colour_4=request.POST['pos4'])
            row.save()
            out = {
                "status": "success",
            }
            return HttpResponse(json.dumps(out))
    else:
        raise HttpResponseNotAllowed(permitted_methods=['POST'])
