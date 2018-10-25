from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class AppSpecie(models.Model):
    name=models.CharField("アプリの種類", max_length=255, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="アプリの種類"

class DjangoProject(models.Model):
    project_name=models.CharField("プロジェクト名", max_length=255, unique=True)
    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name_plural="プロジェクト"


class DjangoApp(models.Model):
    project=models.ForeignKey(DjangoProject, on_delete=models.CASCADE, verbose_name="プロジェクト名")
    appNo=models.CharField("アプリＩＤ", max_length=10)
    app_name=models.CharField("アプリ名", max_length=255)
    app_specie=models.ForeignKey(AppSpecie, on_delete=models.CASCADE, verbose_name="アプリの種類")    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255, primary_key=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    def __str__(self):
        return self.app_name
    class Meta:
        verbose_name_plural="アプリ"




class AppType_1(models.Model):
    """
    関数view_モデルなし
    """
    object_id=models.CharField(max_length=255, primary_key=True, verbose_name="オブジェクトID")
    appNo=models.CharField("アプリＮｏ", max_length=10)
    app_name=models.ForeignKey(DjangoApp, on_delete=models.CASCADE, verbose_name="アプリ名")
    indexURL=models.CharField("indexページのURL",max_length=255)
    def __str__(self):
        return str(self.pk)
    class Meta:
        verbose_name_plural="AppType_1フォーム（関数view_モデルなし）"