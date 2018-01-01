import time
import hashlib
import struct
from django.db import models

COLOUR_CHOICES = (
    ('R', 'Red'),
    ('G', 'Green'),
    ('BU', 'Blue'),
    ('Y', 'Yellow'),
    ('W', 'White'),
    ('BA', 'Black'),
)


def gen_game_id():
    return hashlib.sha224(struct.pack("d", time.time())).hexdigest()[0:6]


class Game(models.Model):
    game_id = models.CharField(max_length=6, primary_key=True, default=gen_game_id)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    code_colour_1 = models.CharField(max_length=2, choices=COLOUR_CHOICES)
    code_colour_2 = models.CharField(max_length=2, choices=COLOUR_CHOICES)
    code_colour_3 = models.CharField(max_length=2, choices=COLOUR_CHOICES)
    code_colour_4 = models.CharField(max_length=2, choices=COLOUR_CHOICES)

    @property
    def guesses_left(self):
        return 10-len(GameRow.objects.filter(game=self))

    @property
    def game_finished(self):
        guesses = GameRow.objects.filter(game=self).order_by('-time')
        if len(guesses) > 0:
            if guesses[0].guess_correct:
                return True
        return self.guesses_left == 0

    def __str__(self):
        return "{}: {}-{}-{}-{}".format(self.game_id, self.code_colour_1, self.code_colour_2,
                                        self.code_colour_3, self.code_colour_4)


class GameRow(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    guess_colour_1 = models.CharField(max_length=2, choices=COLOUR_CHOICES)
    guess_colour_2 = models.CharField(max_length=2, choices=COLOUR_CHOICES)
    guess_colour_3 = models.CharField(max_length=2, choices=COLOUR_CHOICES)
    guess_colour_4 = models.CharField(max_length=2, choices=COLOUR_CHOICES)

    @property
    def num_black_pegs(self):
        total = 0
        for i in range(1, 5):
            if getattr(self.game, "code_colour_{}".format(i)) == getattr(self, "guess_colour_{}".format(i)):
                total += 1
        return total

    @property
    def num_white_pegs(self):
        total = 0
        used = []
        for i in range(1, 5):
            if getattr(self.game, "code_colour_{}".format(i)) == getattr(self, "guess_colour_{}".format(i)):
                used.append(i)
        for j in range(1, 5):
            for i in range(1, 5):
                if i == j:
                    continue
                if getattr(self, "guess_colour_{}".format(i)) == getattr(self.game, "code_colour_{}".format(j))\
                        and j not in used:
                    used.append(j)
                    total += 1
                    break
        return total

    @property
    def guess_correct(self):
        return self.num_black_pegs == 4

    def __str__(self):
        return "{}: {}-{}-{}-{}".format(self.game.game_id, self.guess_colour_1, self.guess_colour_2,
                                        self.guess_colour_3, self.guess_colour_4)

