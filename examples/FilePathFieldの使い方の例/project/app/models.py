from django.db import models

class Django_Project(models.Model):
    project_path=models.FilePathField(path="C:\\Users\\fujita\\PycharmProjects", recursive=False, allow_folders=True, allow_files=False)
