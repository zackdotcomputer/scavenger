from .models import Player, TeamGameProgress
from .util import getPlayerForUser
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def index(request):
  return render(request, 'server/index.html', {'currentPage': 'index'})

@login_required
def profile(request):
  player = getPlayerForUser(request)

  if (player is None):
    return HttpResponseRedirect(reverse('logout'))

  if ('phonenumber' in request.POST):
    player.phone = request.POST['phonenumber'];
    if (not player.phone.startswith('+')):
      player.phone = '+1' + player.phone
    player.save()

  return render(request, 'server/profile.html', {'currentPage': 'profile', 'player': player})

@login_required
def progress(request):
  player = getPlayerForUser(request)

  if (player is None)
    return HttpResponseRedirect(reverse('logout'))

  teams = player.team_set.all()
  activeGames = []
  inactiveGames = []
  for team in teams:
    if (team.game.isActive()):
      activeGames.append(TeamGameProgress(team, Progress.objects.filter(team=team)))
    else:
      inactiveGames.append(TeamGameProgress(team, Progress.objects.filter(team=team)))

  return render(request, 'server/progress.html', {
    'currentPage': 'profile', 'player': player, 'games': activeGames, 'oldGames': inactiveGames
  })
