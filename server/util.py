import os
import foursquare
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Player

def foursquareClient():
  return foursquare.Foursquare(
    client_id=os.environ['FOURSQ_ID'],
    client_secret=os.environ['FOURSQ_SECRET'],
    redirect_uri=os.environ['BASE_HOST'] + reverse('login')
  )

def getPlayerForUser(request):
  try:
    return Player.objects.get(user=request.user)
  except ObjectDoesNotExist as e:
    return None
