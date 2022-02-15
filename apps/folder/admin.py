from django.contrib import admin
from apps.folder.models import *
# Register your models here.

admin.site.register(Folder)
admin.site.register(FolderInFolder)
