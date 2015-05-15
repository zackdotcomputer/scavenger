import json
import logging
import os
from . import util
from .models import Player
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from six import string_types

logger = logging.getLogger('django')

@csrf_exempt
def loginPage(request):
  if (request.user.is_authenticated()):
    # TODO(zack): Support for the next parameter
    return HttpResponseRedirect(reverse('profile'))

  hasLoginError = False

  foursquare = util.foursquareClient()

  if ('code' in request.GET):
    logger.info("Attempting log in for user")
    if (handleCodeFlow(request, str(request.GET['code']), foursquare) and
      ensureUserExistsAndLogin(request, foursquare)):
      # TODO(zack): Support for the next parameter
      return HttpResponseRedirect(reverse('profile'))
    else:
      hasLoginError = True

  context = { 'auth_url': foursquare.oauth.auth_url(), 'currentPage': 'login' }
  return render(request, 'server/login.html', context)

def handleCodeFlow(request, code, foursquare):
  access_token = foursquare.oauth.get_token(code)
  if (isinstance(access_token, string_types) and len(access_token) > 0):
    logger.info("Successfully logged in")
    foursquare.set_access_token(access_token)
    return True

  logger.error("Did not get good Access Token")
  return False

def ensureUserExistsAndLogin(request, foursquare):
  resp = foursquare.users()

  if ("user" in resp):
    me = resp["user"]
    uid = -1
    try:
      uid = long(me["id"])
    except e:
      pass

    if uid > 0:
      try:
        existing = Player.objects.get(foursqId=uid)
      except ObjectDoesNotExist as e:
        existing = None
      password = str(uid) + os.environ['PASSWORD_SECRET'] # never user-facing

      logger.info("Trying to load player")

      if existing is not None and existing.user is not None:
        logger.info("Attempting log in to existing player and user")
        user = authenticate(username=existing.user.username, password=password)
        if user is not None:
          if user.is_active:
            logger.info("Completed log in to existing player and user")
            login(request, user)
            return True
      else:
        email = me.get('contact', {}).get('email', '')
        phone = me.get('contact', {}).get('phone', '')
        if (not phone.startswith("+")):
          if (phone.startswith("1")):
            phone = "+" + phone
          else:
            phone = "+1" + phone

        theUser = User.objects.create_user(str(uid), email, password)
        theUser.first_name = me.get('firstName', '')
        theUser.last_name = me.get('lastName', '')
        theUser.save()

        thePlayer = existing
        if thePlayer is None:
          thePlayer = Player(user=theUser, phone=phone, foursqId=uid)
        else:
          thePlayer.user = theUser
          thePlayer.phone = phone

        thePlayer.save()

        return True

  return False

def handleLogout(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))
