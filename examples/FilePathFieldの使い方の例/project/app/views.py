from django.shortcuts import render
from .forms import Form

def index(request):
    return render(request, 'app/index.html', {"form":Form})

