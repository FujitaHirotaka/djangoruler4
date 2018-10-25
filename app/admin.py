from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *

admin.site.register(AppSpecie)
admin.site.register(DjangoProject)
admin.site.register(DjangoApp)
admin.site.register(AppType_1)


# Register your models here.
