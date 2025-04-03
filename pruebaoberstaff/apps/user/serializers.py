from rest_framework import serializers
from apps.system.models import login

from .models import user, rol, Contacto



class RolSerializers(serializers.ModelSerializer):
	class Meta:

		model = rol
		fields = ('pk_publica', 'Nombre','avatars',"centro_inteligencia", 'social_listening', 'ai_listening' ) 

	def __str__(self):

		return self.RolSerializers

class UsuarioPresentacionSerializer(serializers.ModelSerializer):
	validacion_lvl1_telefono = serializers.CharField(read_only=True)
	validacion_lvl2_email = serializers.CharField(read_only=True)
	rol = RolSerializers(read_only=True)
	class Meta:

		model = user
		fields = ('pk_publica', 'username','email', 'Nombres','validacion_lvl1_telefono', 'validacion_lvl2_email', 'Apellidos', "Contacto", "rol" ) 

	def __str__(self):

		return self.UsuarioPresentacionSerializer




class UsuarioSerializer(serializers.ModelSerializer):
	# rol = RolSerializers(read_only=True)
	rol =serializers.SlugRelatedField(queryset =rol.objects.all(), slug_field='pk_publica')

	class Meta:

		model = user
		fields = ('pk_publica','username','password','email', 'Nombres', 'Apellidos','rol', "Contacto","Comentarios" ) 

	def __str__(self):

		return self.UsuarioSerializer


class UsuarioLisSerializer(serializers.ModelSerializer):
	rol = RolSerializers(read_only=True)

	class Meta:

		model = user
		fields = ('pk_publica','username','email', 'Nombres', 'Apellidos','rol' ) 

	def __str__(self):

		return self.UsuarioSerializer

	
class LoginSerializer(serializers.ModelSerializer):

	class Meta:

		model = login
		fields = ('email', 'password') 

	def __str__(self):

		return self.LoginSerializer
	

class ContactoSerializers(serializers.ModelSerializer):
	# user = UsuarioSerializer(read_only=True)
	class Meta:

		model = Contacto
		fields = ('pk_publica', 'Nombres', 'Apellidos', 'Telefono', 'Correo',) 
	def __str__(self):

		return self.ContactoSerializers