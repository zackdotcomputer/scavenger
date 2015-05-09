from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
  if (request.method == 'POST'):
    return handleLogin(request)
  return HttpResponse("Hello, world. You're at the login page.")

def handleLogin(request):
  return HttpResponse("Hello, world. You're POSTing to the login page.")
