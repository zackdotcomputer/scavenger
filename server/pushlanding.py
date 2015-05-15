import logging
import os
import json
from . import util
from .models import Game, Player, Progress
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('django')

@csrf_exempt
def handle(request):
  if (request.method != 'POST'):
    raise Http404

  if (not Game.objects.all()[0].isActive()):
    logger.info("Ignoring push because game is not active")
    return HttpResponse("")

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
    if (nextClue is not None):
      if (venueId in nextClue.solutionsIdsList()):
        Progress(team=player.team, clue=nextClue).save() # mark this clue complete
        sendHintToNextClue(player)
      elif (venueId == Game.objects.all()[0].initialVenueId):
        sendHintToNextClue(player)
  else:
    logger.error("Push notification for unknown user ID: " + str(uid))

  return HttpResponse("") # Generic 200

def sendHintToNextClue(player):
  if (len(player.phone) < 1):
    logger.error("No Phone! Can't send clue to player " + str(player.foursqId))
  else:
    nextClue = player.team.nextIncompleteClue();
    client = util.twilioClient()

    if (nextClue is not None):
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
    else:
      message = client.messages.create(
        body = "Congratulations, you've found all the venues for your team! Enjoy the rest of your day!",
        to = player.phone,    # Replace with your phone number
        from_ = os.environ['TWILIO_PHONE']
      )

      logger.info("Sent game completion to player id " + str(player.foursqId) + " with message sid " + message.sid)
