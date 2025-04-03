import uuid
from datetime import datetime
from django.db import models
from apps.system.models import basemodel
from apps.user.models import user, Contacto
# Create your models here.



class Proyecto(basemodel):
	
	Nombre = models.CharField(max_length=100, help_text='Nombre del Proyecto')
	Descripcion = models.CharField(max_length=500, help_text="Descripcion del proyecto", null=True, default="")
	
	FechaDeInicio = models.DateTimeField( help_text="fecha a iniciar", default=datetime.now())
	FechaDeFin = models.DateTimeField( help_text="fecha de fin", default=datetime.now())
	estados =  (('Pendiente','Pendiente'), ('Completado','Completado'), ('En progreso','En progreso'), ('Cancelado','Cancelado'))
	Estado =  models.CharField(max_length=20, choices=estados, default='En progreso')

	AlertaDiaria = models.BooleanField(default=False)
	AlertaSemanal = models.BooleanField(default=False)
	TormentaDeAlerta = models.BooleanField(default=False)
	creador = models.ForeignKey(user,
								related_name="userproyecto", 
								null=True, 
								blank=True,
								default=None,
								on_delete=models.CASCADE)
	asignados = models.ManyToManyField(Contacto, default=None, related_name="asignaciones")
	def permisos():

		permisos = {
			'Administrador' : ('get','post','put', 'delete'),
			'Colaborador' : ('get','post', 'put', 'delete'),
			'Observador' : ('get'),
		}

		return permisos

class emailreportes(basemodel):
	email = models.CharField(max_length=100, default='')
	proyecto =  models.ForeignKey(Proyecto,
								related_name="emailreportes", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	def permisos():

		permisos = {
			'Administrador' : ('get','post','put', 'delete'),
			'Colaborador' : ('get'),
			'Observador' : ('get'),
		}
		return permisos


class tarea(basemodel):
	
	Nombre = models.CharField(max_length=100, default="")
	Descripcion = models.CharField(max_length=500, default="")
	estados =  (('Pendiente','Pendiente'), ('Completado','Completado'), ('En progreso','En progreso'), ('Cancelado','Cancelado'))
	Estado =  models.CharField(max_length=20, choices=estados, default='En progreso')
	Fecha_vencimiento = models.DateTimeField(default=datetime.now())
	asignado = models.ForeignKey(Contacto,
								related_name="tareauser",
								null=True,
								blank=True,
								default=None,
								on_delete=models.CASCADE)
	proyecto = models.ForeignKey(Proyecto,
								related_name="proyectotarea",
								null=True,
								blank=True,
								default=None,
								on_delete=models.CASCADE)


class comentario(basemodel):
	comentario = models.CharField(max_length=500, default="")
	tarea = models.ForeignKey(tarea,
								related_name="tareacomentario",
								null=True,
								blank=True,
								default=None,
								on_delete=models.CASCADE)
	usuario = models.ForeignKey(user,
								related_name="comentariotarea",
								null=True,
								blank=True,
								default=None,
								on_delete=models.CASCADE)




