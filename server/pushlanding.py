import logging
import os
import json
from .models import Game, Player, Progress
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from twilio.rest import TwilioRestClient

logger = logging.getLogger('django')

@csrf_exempt
def handle(request):
  if (request.method != 'POST'):
    raise Http404

  logger.info("Received a push notification")

  rawCheckin = request.POST['checkin']
  checkin = json.loads(rawCheckin)

  # Process is to load the user for the push, see if the check-in meets a clue, update progress, then send a clue
  uid = checkin['user']['id']
  venueId = checkin['venue']['id']
  try:
    player = Player.objects.get(foursqId=uid)
  except ObjectDoesNotExist as e:
    player = None

  if (player is not None and len(venueId) > 0):
    nextClue = player.team.nextIncompleteClue()
    if (venueId in nextClue.solutionsIdsList()):
      Progress(team=team, clue=clue).save() # mark this clue complete
      sendHintToNextClue(player)
    elif (venueId == Game.objects.all()[0].initialVenueId):
      sendHintToNextClue(player)
  else:
    logger.error("Push notification for unknown user ID: " + str(uid))

  return HttpResponse("") # Generic 200

def sendHintToNextClue(player):
  nextClue = player.team.nextIncompleteClue();
  account_sid = os.environ['TWILIO_SID']
  auth_token  = os.environ['TWILIO_AUTH_TOKEN']
  client = TwilioRestClient(account_sid, auth_token)

  message = client.messages.create(
    body = nextClue.hint,
    to = player.phone,    # Replace with your phone number
    from_ = os.environ['TWILIO_PHONE']
  )

  logger.info("Sent clue to player id " + str(player.foursqId) + " with message sid " + message.sid)

  if (len(nextClue.bonus) > 0):
    bonusSid = client.messages.create(
      body = nextClue.bonus,
      to = player.phone,    # Replace with your phone number
      from_ = os.environ['TWILIO_PHONE']
    )
    logger.info("Sent bonus to player id " + str(player.foursqId) + " with message sid " + message.sid)
