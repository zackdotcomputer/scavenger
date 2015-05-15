import os
from .models import Player, Game
from .util import getPlayerForUser, twilioClient
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

logger = logging.getLogger('django')

def index(request):
  return render(request, 'server/index.html', {'currentPage': 'index'})

@login_required
def profile(request):
  player = getPlayerForUser(request)

  if (player is None):
    return HttpResponseRedirect(reverse('logout'))

  updatedUser = False
  if ('phonenumber' in request.POST):
    player.phone = request.POST['phonenumber'];
    if (not player.phone.startswith("+")):
      if (player.phone.startswith("1")):
        player.phone = "+" + player.phone
      else:
        player.phone = "+1" + player.phone

    player.save()
    updatedUser = True

    if ('sendText' in request.POST):
      client = twilioClient()
      message = client.messages.create(
        body = "Yeah, it worked",
        to = player.phone,    # Replace with your phone number
        from_ = os.environ['TWILIO_PHONE']
      )
      logger.info("Sent test ping to player id " + str(player.foursqId) + " with message sid " + message.sid)

  return render(request, 'server/profile.html', {'currentPage': 'profile', 'player': player, 'updated': updatedUser})

@login_required
def progress(request):
  player = getPlayerForUser(request)

  if (player is None):
    return HttpResponseRedirect(reverse('logout'))

  if (not Game.objects.all()[0].isActive()):
    return render(request, 'server/inactive.html', {
      'currentPage': 'progress',
      'player': player
    })

  progressPercent = float(0)
  if (player.team.totalClueCount() > 0):
    progressPercent = (float(player.team.completedClueCount()) / float(player.team.totalClueCount()))

  return render(request, 'server/progress.html', {
    'currentPage': 'progress',
    'player': player,
    'clues': player.team.completedCluesAndNext(),
    'progressPercent': progressPercent
  })
