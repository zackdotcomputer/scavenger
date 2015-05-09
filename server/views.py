from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
  return render(request, 'server/index.html', {})

@login_required
def profile(request):
  return HttpResponse("Hello, world. You're at the profile page.")

@login_required
def progress(request):
  return HttpResponse("Hello, world. You're at the progress page.")
