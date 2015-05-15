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

  def solutionsIdsList(self):
    return self.solutions.split(',')

class Team(models.Model):
  name = models.CharField('team name', max_length=200)
  course = models.ManyToManyField(Clue)
  courseOrder = models.CharField('course order', max_length=200, default='')
  def __unicode__(self):
    return 'Team: ' + self.name

  def members(self):
    return ', '.join(player.displayName() for player in self.player_set.all())

  def completedClueCount(self):
    return self.progress_set.count()

  def totalClueCount(self):
    return self.course.count()

  def completedCluesAndNext(self):
    result = [];
    explodedIds = self.courseOrder.split(',')
    for clueId in explodedIds:
      hasMatch = (Progress.objects.filter(team=self, clue_id=int(clueId)).count() > 0)
      for clue in self.course.all():
          if str(clue.id) == clueId:
            result.append(clue)
            break;

      if not hasMatch:
        break

    return result

  def nextIncompleteClue(self):
    explodedIds = self.courseOrder.split(',')
    for clueId in explodedIds:
      hasMatch = (Progress.objects.filter(team=self, clue_id=int(clueId)).count() > 0)
      if not hasMatch:
        for clue in self.course.all():
          if str(clue.id) == clueId:
            return clue

    return None

class Player(models.Model):
  user = models.OneToOneField(User, blank=True, null=True)
  phone = models.CharField('Phone number', max_length=40, blank=True, default='')
  shortname = models.CharField('Name', max_length=100, blank=True, default='')
  foursqId = models.BigIntegerField('Foursquare User ID')
  team = models.ForeignKey(Team, null=True)
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
  time = models.DateTimeField('solution time', auto_now_add=True)

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
