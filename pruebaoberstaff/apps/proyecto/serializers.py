from rest_framework import serializers
from .models import Proyecto, emailreportes, tarea, comentario
from apps.user.serializers import ContactoSerializers, UsuarioLisSerializer
from apps.user.models import Contacto, user


class ProyectoSerializer(serializers.ModelSerializer):

	asignados = ContactoSerializers(many=True, read_only=True)  
	asignados_pk_publica = serializers.SlugRelatedField(
        queryset=Contacto.objects.all(),
		slug_field='pk_publica',
        source='asignados',
        many=True,
        write_only=True
    )
	class Meta:

		model = Proyecto
		fields = ('pk_publica','Nombre','Descripcion', 'FechaDeInicio', 'FechaDeFin', 'Estado', 'AlertaDiaria', 'AlertaSemanal', 'TormentaDeAlerta', 'asignados', 'asignados_pk_publica') 

	



class emailreporteSerializer(serializers.ModelSerializer):

	proyecto = serializers.SlugRelatedField(queryset=Proyecto.objects.all(), slug_field='pk_publica')
	email = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False
    )
	class Meta:

		model = emailreportes
		fields = ('pk_publica','email','proyecto') 

	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.proyecto = validated_data.get('proyecto', instance.proyecto)
		
		
		instance.save()
		return instance


class tareaSerializers(serializers.ModelSerializer):
	asignado = ContactoSerializers(many=False, read_only=True)  
	asignado_pk_publica = serializers.SlugRelatedField(
        queryset=Contacto.objects.all(),
		slug_field='pk_publica',
        source='asignado',
        many=False,
        write_only=True
    )
	proyecto = ProyectoSerializer(many=False, read_only=True)  
	proyecto_pk_publica = serializers.SlugRelatedField(
        queryset=Proyecto.objects.all(),
		slug_field='pk_publica',
        source='proyecto',
        many=False,
        write_only=True
    )
	
	class Meta:

		model = tarea
		fields = ('pk_publica','Nombre', 'Descripcion', 'Estado', 'asignado', 'asignado_pk_publica','proyecto', 'proyecto_pk_publica') 




class comentarioSerializers(serializers.ModelSerializer):
	tarea = serializers.SlugRelatedField(
        queryset=tarea.objects.all(),
		slug_field='pk_publica',
        # source='tarea',
        # many=False,
        # write_only=True
    )
	# usuario = UsuarioLisSerializer(many=False,read_only=True)
	class Meta:
		model = comentario
		fields = ('pk_publica', 'comentario', 'tarea', )







