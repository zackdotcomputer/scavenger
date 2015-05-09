from .models import Player
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def index(request):
  return render(request, 'server/index.html', {'currentPage': 'index'})

@login_required
def profile(request):
  try:
    player = Player.objects.get(user=request.user)
  except ObjectDoesNotExist as e:
    HttpResponseRedirect(reverse('logout'))

  if ('phonenumber' in request.POST):
    player.phone = request.POST['phonenumber'];
    if (not player.phone.startswith('+')):
      player.phone = '+1' + player.phone
    player.save()

  return render(request, 'server/profile.html', {'currentPage': 'profile', 'player': player})

@login_required
def progress(request):
  return HttpResponse("Hello, world. You're at the progress page.")
