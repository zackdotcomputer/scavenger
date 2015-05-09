from django.contrib import admin

from .models import Player, Game, Clue, Team

class ClueInline(admin.StackedInline):
  model = Clue
  extra = 5

class GameAdmin(admin.ModelAdmin):
  fieldsets = [
    (None,               {'fields': ['name']}),
    ('Valid from', {'fields': ['start_time', 'end_time']}),
  ]
  inlines = [ClueInline]


admin.site.register(Player)
admin.site.register(Game, GameAdmin)
admin.site.register(Clue)
admin.site.register(Team)
