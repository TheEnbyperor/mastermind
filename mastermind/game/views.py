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

