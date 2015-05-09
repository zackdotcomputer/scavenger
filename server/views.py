from django.http import HttpResponse
from django.shortcuts import render

def index(request):
  return render(request, 'server/index.html', {})

def profile(request):
  return HttpResponse("Hello, world. You're at the profile page.")

def progress(request):
  return HttpResponse("Hello, world. You're at the progress page.")
