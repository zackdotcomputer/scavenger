from .models import Player
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
    if (not player.phone.startswith("+")):
      if (player.phone.startswith("1")):
        player.phone = "+" + player.phone
      else:
        player.phone = "+1" + player.phone

    player.save()

  return render(request, 'server/profile.html', {'currentPage': 'profile', 'player': player})

@login_required
def progress(request):
  player = getPlayerForUser(request)

  if (player is None):
    return HttpResponseRedirect(reverse('logout'))

  return render(request, 'server/progress.html', {
    'currentPage': 'progress',
    'player': player,
    'clues': player.team.completedCluesAndNext(),
    'progressPercent': (float(player.team.completedClueCount()) / float(player.team.totalClueCount()))
  })
