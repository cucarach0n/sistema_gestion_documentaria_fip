from django.contrib import admin
from apps.users.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('id','password','correo','nombreUsuario','name','last_name','avatar')

admin.site.register(User,UserAdmin)