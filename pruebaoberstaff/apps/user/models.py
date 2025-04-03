import uuid
from django.db import models
from apps.system.models import basemodel

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class rol(basemodel):

	Nombre = models.CharField(max_length=15)
	avatars = models.BooleanField(default=False)
	centro_inteligencia = models.BooleanField(default=False)
	social_listening = models.BooleanField(default=False)
	ai_listening = models.BooleanField(default=False)

	
	def permisos():

		permisos = {
			'Admin' : ('get','post','update', 'delete'),
			'Coordinador' : ('get','post','update', 'delete'),
			'Servicio' : ('get','post','update', 'delete'),
		}

		return permisos

	def __str__(self):
		return self.Nombre

class UserManager(BaseUserManager):
	""" Modelo que hereda de la clase base que usa django para generar 
	los usuarios, de esta forma podemos personalizar los campos 
	necesarios para generar el usuario que creamos en la consola
	con el comando "python manage.py createsuperuser" """

	def _create_user(self, email, password, 
					is_staff, is_superuser, **extra_field):
		
		if not email:
			raise ValueError("El campo email es necesario")
		email = self.normalize_email(email)
		print()
		print()
		print( email, True, is_staff,
							is_superuser, **extra_field)
		user = self.model(email=email, is_active=True, is_staff=is_staff,
							is_superuser=is_superuser, **extra_field)
		user.set_password(password)
		user.save(using = self._db)

		return user

	def create_user(self, email, password=None, **extra_field):
		return self._create_user(email, password, False, False,  **extra_field)

	def create_superuser(self, email, password, **extra_field):
		return self._create_user(email, password, True, True,  **extra_field)


class user(AbstractBaseUser, PermissionsMixin):

	""" Modelo usado para generar al usuario que se maneja en el contexto de la
	plataforma.
	Hereda propiedades de  AbstractBaseUser  y PermissionsMixin para que el modelo
	a pesar de ser personalizado pueda ser usado por django en sus subrutinas de 
	verificación y validación. """

	pk_publica = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	Creado = models.DateTimeField(auto_now_add=True)
	Modificado =models.DateTimeField(auto_now=True)
	username = models.CharField(max_length=15)
	email = models.EmailField(max_length=50, unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	Status = models.BooleanField(default=True)
	Nombre_completo = models.CharField(max_length=60, default="")
	Nombres = models.CharField(max_length=50, default="")
	Apellidos = models.CharField(max_length=50, default="")
	Contacto = models.CharField(max_length=50, default="")
	Comentarios = models.CharField(max_length=200, default="")
	rol = models.ForeignKey(rol,
								related_name="roluser", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE, 
								default = 1)
	Codigo = models.CharField(max_length=60, blank=True, null=True)
	validacion_lvl1_telefono =  models.BooleanField(default=False)
	validacion_lvl2_email =  models.BooleanField(default=False)
	lat = models.CharField(max_length=60, blank=True, null=True)
	log = models.CharField(max_length=60, blank=True, null=True)
	objects = UserManager() 

	USERNAME_FIELD = 'email'


	def get_short_name(self):
		return self.username

	
	def permisos():

		permisos = {
			'Admin' : ('get','post','update', 'delete'),
			'Coordinador' : ('get','post','update', 'delete'),
			'Servicio' : ('get','post','update', 'delete'),
		}
		return permisos




class Token(basemodel):


	token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	user = models.ForeignKey(user,
								related_name="Token", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	def permisos():

		permisos = {
			'Admin' : ('get','post','update', 'delete'),
			'Coordinador' : ('get','post','update', 'delete'),
			'Servicio' : ('get','post','update', 'delete'),
		}

		return permisos
	
class keysRecovery(basemodel):

	user = models.ForeignKey(user,
								related_name="keysRecovery", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	keysRecovery = models.CharField(max_length=15, blank=True, null=True)



class Contacto(basemodel):

	Nombres = models.CharField(max_length=50, default="")
	Apellidos = models.CharField(max_length=50, default="")
	Telefono = models.CharField(max_length=50, default="")
	Correo = models.CharField(max_length=50)
	to_user = models.ForeignKey(user,
								related_name="contactosuser", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	ref = models.ForeignKey(user,
								related_name="referenciacontacto", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)