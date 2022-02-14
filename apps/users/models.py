from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from apps.sgdapi.models import UnidadArea


class UserManager(BaseUserManager):
    def _create_user(self, nombreUsuario, correo, name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            nombreUsuario = nombreUsuario,
            correo = correo,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, nombreUsuario, correo, name,last_name, password=None, **extra_fields):
        return self._create_user(nombreUsuario, correo, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, nombreUsuario, correo, name,last_name, password=None, **extra_fields):
        return self._create_user(nombreUsuario, correo, name,last_name, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    nombreUsuario = models.CharField('Usuario',max_length = 255, unique = True)
    correo = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    avatar = models.ImageField('Imagen de perfil', upload_to='avatars/', max_length=255, null=True, blank = True)
    estado = models.SmallIntegerField('Estado del usuario',null = True, default=0, blank = False)
    #unidadArea = models.ForeignKey("UnidadArea",on_delete=models.CASCADE)
    is_active = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombreUsuario','name','last_name']

    def __str__(self):
        return f'{self.correo} {self.nombreUsuario}'