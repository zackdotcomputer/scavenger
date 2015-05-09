from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

@csrf_exempt
def login(request):
  if (request.method == 'POST'):
    return handleLogin(request)
  return HttpResponse("Hello, world. You're at the login page.")

def handleLogin(request):
  return HttpResponse("Hello, world. You're POSTing to the login page.")

def handleLogout(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))