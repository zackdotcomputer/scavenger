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
    if (not phone.startswith("+")):
      if (phone.startswith("1")):
        phone = "+" + phone
      else:
        phone = "+1" + phone

    player.save()

  return render(request, 'server/profile.html', {'currentPage': 'profile', 'player': player})

@login_required
def progress(request):
  player = getPlayerForUser(request)

  if (player is None):
    return HttpResponseRedirect(reverse('logout'))

  return render(request, 'server/progress.html', {
    'currentPage': 'profile', 'player': player
  })
