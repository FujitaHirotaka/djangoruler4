from django.shortcuts import render
from django.http import HttpResponse
import os
from pathlib import Path
from .forms import Form

#家と学校の環境でベースパスを使い分ける
pathlist=["C://users/sakodaken/pycharmprojects", "C://users/fujita/pycharmprojects"]
for i in pathlist:
    if Path(i).exists():
          directory_of_projects=Path(i)/"djangoruler3"/"project"/"app_example"



def index(request):
    print(directory_of_projects)
    return render(request, 'app_example/index.html', {"form":Form})
