import os
import foursquare
from django.core.urlresolvers import reverse

def foursquareClient():
  return foursquare.Foursquare(
    client_id=os.environ['FOURSQ_ID'],
    client_secret=os.environ['FOURSQ_SECRET'],
    redirect_uri=os.environ['BASE_HOST'] + reverse('login')
  )