from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
  user = models.OneToOneField(User, blank=True, null=True)
  phone = models.CharField('Phone number', max_length=40, blank=True, default='')
  shortname = models.CharField('Name', max_length=100, blank=True, default='')
  foursqId = models.BigIntegerField('Foursquare User ID')
  def __unicode__(self):
    return 'User: ' + str(self.foursqId)

  def email(self):
    if (self.user is not None and self.user.email is not None):
      return self.user.email

    return None

  def foursquareProfileHref(self):
    return 'https://foursquare.com/user/' + str(self.foursqId)

  def displayName(self):
    result = ''
    if (self.user is not None):
      if (len(self.user.first_name) > 0):
        result += self.user.first_name
        if (len(self.user.last_name) > 0):
          result += ' '
      if (len(self.user.last_name) > 0):
          result += self.user.last_name
    elif (self.shortname is not None):
      result = self.shortname

    return result

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
