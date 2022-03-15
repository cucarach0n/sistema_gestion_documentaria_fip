from django.contrib import admin

from apps.share.models import FileShare, FolderShare

# Register your models here.
admin.site.register(FolderShare)
admin.site.register(FileShare)