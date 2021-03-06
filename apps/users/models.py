from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords
from apps.unidadArea.models import UnidadArea


class UserManager(BaseUserManager):
    def _create_user(self, correo, name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
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

    def create_user(self, correo, name,last_name, password=None, **extra_fields):
        return self._create_user( correo, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, correo, name,last_name, password=None, **extra_fields):
        return self._create_user(correo, name,last_name, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    #nombreUsuario = models.CharField('Usuario',max_length = 255, unique = True)
    correo = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    avatar = models.ImageField('Imagen de perfil', upload_to='avatars/', default="avatars/avataruni.png",max_length=255, null=True, blank = True)
    estado = models.SmallIntegerField('Estado del usuario',null = True, default=1, blank = False)
    unidadArea = models.ForeignKey(UnidadArea, on_delete=models.CASCADE,null =True,blank=True)
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now_add=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now=True)
    is_active = models.BooleanField(default = True)
    is_staff = models.SmallIntegerField('Staff',null = True, default=1, blank = True)
    historical = HistoricalRecords(excluded_fields=['name','last_name','avatar','estado','unidadArea','is_active','is_staff','correo','password','last_login','is_superuser'])
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['name','last_name']

    def __str__(self):
        return f'{self.correo} {self.name}'


class Contrasena_reinicio(models.Model):
    id = models.AutoField(primary_key = True)
    correo = models.EmailField('Correo usuario',max_length=255,null = False, blank = False, unique=True)
    token = models.CharField('token validador',max_length=40,null = False, blank = False, unique=True)
    fechaCambio = models.DateTimeField('Fecha de Cambio',auto_now = False,auto_now_add = True) 
    estado = models.SmallIntegerField('Estado del token',null = True, default=1, blank = False)
    usuario = models.ForeignKey("User", on_delete=models.CASCADE)
    historical = HistoricalRecords(excluded_fields=['correo','token','fechaCambio','estado','usuario',])

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Contrasena_reinicio'
        verbose_name_plural = 'Contrasenas_reinicios'
    
    def __str__(self):
        return "{0},{1}".format(self.correo,self.fechaCambio)