import logging
import os
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from twilio.rest import TwilioRestClient

logger = logging.getLogger('django')

@csrf_exempt
def handle(request):
  if (request.method != 'POST'):
    raise Http404
  return HttpResponse("Hello, world. You're at the push page.")

def testSms(request):
  # Your Account Sid and Auth Token from twilio.com/user/account
  account_sid = os.environ['TWILIO_SID']
  auth_token  = os.environ['TWILIO_AUTH_TOKEN']
  client = TwilioRestClient(account_sid, auth_token)

  message = client.messages.create(
    body="Jenny please?! I love you <3",
    to="+19172679225",    # Replace with your phone number
    from_=os.environ['TWILIO_PHONE']
  )
  logger.info(message.sid)
  return HttpResponse(message.sid)
