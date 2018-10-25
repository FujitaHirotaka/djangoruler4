from django.db import models
from pathlib import Path
import os

pathlist=["C://users/sakodaken/pycharmprojects", "C://users/fujita/pycharmprojects"]
for i in pathlist:
    if Path(i).exists():
          directory_of_projectexamples=Path(i)/"djangoruler3"/"project"

class Django_Project(models.Model):
    example_path=models.FilePathField(path=directory_of_projectexamples, recursive=False, allow_folders=True, allow_files=False)
