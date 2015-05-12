from django.db import models
from django.contrib.auth.models import User
import datetime

class Clue(models.Model):
  hint = models.CharField('Clue hint text', max_length=200)
  bonus = models.CharField('Optional bonus text', max_length=200, default='', blank=True)
  # max solutions = 8 at 24 characters per id plus 1 separating comma
  solutions = models.CharField('Comma separated Foursquare venue ID solutions', max_length=200)
  def __unicode__(self):
    return 'Clue: ' + self.hint

class Team(models.Model):
  name = models.CharField('team name', max_length=200)
  course = models.ManyToManyField(Clue)
  courseOrder = models.CharField('course order', max_length=200, default='')
  def __unicode__(self):
    return 'Team: ' + self.name

  def members(self):
    return ', '.join(player.displayName() for player in self.player_set.all())

class Player(models.Model):
  user = models.OneToOneField(User, blank=True, null=True)
  phone = models.CharField('Phone number', max_length=40, blank=True, default='')
  shortname = models.CharField('Name', max_length=100, blank=True, default='')
  foursqId = models.BigIntegerField('Foursquare User ID')
  team = models.ForeignKey(Team)
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

class Progress(models.Model):
  team = models.ForeignKey(Team)
  clue = models.ForeignKey(Clue)
  time = models.DateTimeField('solution time')

class Game(models.Model):
  name = models.CharField('name', max_length=200)
  start_time = models.DateTimeField('game start')
  end_time = models.DateTimeField('game end')
  cluesPer = models.IntegerField('clues per team', default=4)
  initialVenueId = models.CharField('inital venue id', max_length=30, default='')

  def isActive(self):
    now = datetime.datetime.now()
    return (now >= start_time and now < end_time)

  def __unicode__(self):
    return 'Game: ' + self.name

# non-persisted convenience object
class TeamGameProgress(object):
  def __init__(self, team, progress):
    self.team = team
    self.progress = progress

  def completedClueCount(self):
    return len(self.progress)

  def totalClueCount(self):
    return len(self.team.course)

  def nextIncompleteClue(self):
    explodedIds = self.team.courseOrder.split(',')
    for clueId in explodedIds:
      hasMatch = False
      for progress in self.progress:
        if str(self.progress.id) == clueId:
          hasMatch = True
          break
      if not hasMatch:
        return clue

    return None
