from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
  user = models.OneToOneField(User)
  phone = models.CharField('Phone number', max_length=40)
  foursqId = models.BigIntegerField('Foursquare User ID')
  def __unicode__(self):
    return 'User: ' + str(self.foursqId)

class Game(models.Model):
  name = models.CharField('name', max_length=200)
  start_time = models.DateTimeField('game start')
  end_time = models.DateTimeField('game end')
  def __unicode__(self):
    return 'Game: ' + self.name

class Clue(models.Model):
  game = models.ForeignKey(Game)
  hint = models.CharField('Clue hint text', max_length=200)
  bonus = models.CharField('Optional bonus text', max_length=200)
  # max solutions = 8 at 24 characters per id plus 1 separating comma
  solutions = models.CharField('Comma separated Foursquare venue ID solutions', max_length=200)
  def __unicode__(self):
    return 'Clue: ' + self.hint

class Team(models.Model):
  name = models.CharField('team name', max_length=200)
  players = models.ManyToManyField(Player)
  course = models.ManyToManyField(Clue)
  def __unicode__(self):
    return 'Team: ' + self.name

class Progress(models.Model):
  team = models.ForeignKey(Team)
  clue = models.ForeignKey(Clue)
  time = models.DateTimeField('solution time')