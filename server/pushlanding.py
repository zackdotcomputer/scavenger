from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handle(request):
  if (request.method != 'POST'):
    raise Http404
  return HttpResponse("Hello, world. You're at the push page.")
