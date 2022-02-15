from django.contrib import admin
from apps.tag.models import *
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    list_display = ('id','tagName','fechaRegistro','fechaUpdate')
admin.site.register(Tag,TagAdmin)