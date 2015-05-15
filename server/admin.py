from django.contrib import admin

import random
from .models import Game, Player, Clue, Team

class ClueInline(admin.StackedInline):
  model = Clue
  extra = 5
  fieldsets = [(None, {'fields': ['hint', 'bonus', 'solutions']})]

class PlayerInline(admin.StackedInline):
  model = Player
  fieldsets = [(None, {'fields': ['shortname', 'foursqId']})]
  extra = 10

def randomizeTeamClues(modeladmin, request, queryset):
  teams = queryset.all()
  clues = list(Clue.objects.all())
  cluesPer = Game.objects.all()[0].cluesPer
  if (cluesPer > len(clues)):
    cluesPer = len(clues)

  for team in teams:
    random.shuffle(clues)
    course = clues[:cluesPer]
    team.course = course
    team.courseOrder = ','.join(str(clue.id) for clue in course)
    team.save()

randomizeTeamClues.short_description = "Assign random clues to selected teams"

class TeamAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,          {'fields': ['name']}),
  ]
  inlines = [PlayerInline]
  list_display = ('name', 'members', 'courseOrder', 'completedClueCount')
  actions = [randomizeTeamClues]

class GameAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,               {'fields': ['name', 'cluesPer', 'initialVenueId']}),
    ('Valid from', {'fields': ['start_time', 'end_time']}),
  ]
  list_display = ('name', 'start_time')

class ClueAdmin(admin.ModelAdmin):
  fieldsets = [(None, {'fields': ['hint', 'bonus', 'solutions']})]
  list_display = ('id', 'hint', 'solutions')

class PlayerAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,          {'fields': ['shortname', 'foursqId', 'phone', 'team']}),
    ('Linked User', {'fields': ['user']}),
  ]
  list_display = ('displayName', 'foursqId', 'phone')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Clue, ClueAdmin)
admin.site.register(Team, TeamAdmin)
