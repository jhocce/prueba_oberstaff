

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.core.paginator import Paginator

from apps.system.ManageApi import ErrorManagerMixin
from apps.system.monitor import MonitorMixin
from apps.user.models import user
from .models import Proyecto, emailreportes, tarea, comentario
from .serializers import ProyectoSerializer, emailreporteSerializer, tareaSerializers
from .serializers import comentarioSerializers


class ProyectoAPI(MonitorMixin, 
            CreateAPIView, 
            ListAPIView, 
            RetrieveAPIView, 
            UpdateAPIView, 
            DestroyAPIView,
            APIView):
	model= Proyecto
	serializer_class = ProyectoSerializer

	def post(self, request, *arg, **kwargs):
		""" Recibe los un json con los datos del proyecto a registrar
		"""
		data = self.get_data_body()
		dataser = self.serializer_class(data=data)
		if dataser.is_valid():
			dataser.validated_data['creador'] = self.usuario
			dataser.save()
			self.MensajeListAdd( mensaje_user = {'mensaje':'El proyecto se registro con exito'}, status='success')
			self.JsonAdd(dataser.data)
			return Response(self.salida(), status=200)
		else:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No se logro registrar el proyecto'}, status='error')
			self.JsonAdd(dataser.errors)
			return Response(self.salida(), status=200)
		
	def get(self, request, *arg, **kwargs):
		
		""" 
		Enviar por get "pkquery" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
				de todos los registros del usuario en cuestion de ser asi enviar: \n
					count: numero de elementos por pagina \n
					page: numero de pagina """
		try:
			if self.pkquery is None:
				
				quey = self.model.objects.filter(Status=True)
				if self.count and self.page:
					paginacion= Paginator(quey,self.count)
					
					if len(paginacion.page(1)) == 0:
						quey = None
					else:
						quey = paginacion.page(self.page)

				if quey is not None:
					total_count = quey.object_list.count()
					f = self.serializer_class(quey, many=True)
					
					
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
					self.MensajeListAdd(mensaje_user =  {'mensaje':'Tu lista de proyectos'}, status="success")
					return Response(self.salida(), status=200)
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'No hay registros'}, status="success")
				return Response(self.salida(), status=200)
			else:
				quey = self.model.objects.filter(Q(pk_publica=self.pkquery)&Q(Status=True)).first()
				if quey is None:
					self.MensajeListAdd(mensaje_user = {'mensaje': 'El proyecto no existe'} ,
						mensaje_server = {'mensaje': 'El proyecto no existe'}, status="success")			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(quey)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

		return Response(self.salida(), status=200)

	def delete(self, request, *arg, **kwargs):
		
		try:
			objeto = self.model.objects.get(Q(pk_publica=self.pkquery)&Q(Status=True))
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = {'mensaje': 'El proyecto a sido eliminado exitosamente'})
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e), status="error")
			
		

		return Response(self.salida(), status=200)


	def update(self, request, *arg, **kwargs):


		data = self.get_data_body()
		
		try:
			
			if self.pkquery is None:
				self.MensajeListAdd(mensaje_user= {'mensaje':'Ocurrieron errores al momento de guardar el proyecto'},
				mensaje_server={'mensaje':'No se a enviado correctamente la variable "pkquery" correspondiente al objeto al cual actualizar en la URL'}, status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
					
					objeto = self.model.objects.get(pk_publica=self.pkquery,
					Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar datos del proyecto'},
						mensaje_server = {'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'})
					return Response(self.salida(), status=404)
				
				usuarioserializer = self.serializer_class( objeto, data= data,partial=True)

				if usuarioserializer.is_valid():
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user={'mensaje':'proyecto Actualizado con exito'}, status='success')
					self.JsonAdd(json =  usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el proyecto'},
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)




class emailreportesAPI(MonitorMixin, 
            CreateAPIView, 
            ListAPIView, 
            RetrieveAPIView, 
            UpdateAPIView, 
            DestroyAPIView,
            APIView):
	model= emailreportes
	serializer_class = emailreporteSerializer

	def post(self, request, *arg, **kwargs):
		""" Recibe los un json con los datos del reporte a registrar
		"""
		data = self.get_data_body()
		dataser = self.serializer_class(data=data)
		if dataser.is_valid():
			# dataser.validated_data['user'] = self.usuario
			dataser.save()
			self.MensajeListAdd( mensaje_user = {'mensaje':'El reporte se registro con exito'}, status='success')
			self.JsonAdd(dataser.data)
			return Response(self.salida(), status=200)
		else:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No se logro registrar el reporte'}, status='error')
			self.JsonAdd(dataser.errors)
			return Response(self.salida(), status=200)
		
	def get(self, request, *arg, **kwargs):
		
		""" 
		Enviar por get "pkquery" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
				de todos los registros del usuario en cuestion de ser asi enviar: \n
					count: numero de elementos por pagina \n
					page: numero de pagina """
		try:
			if self.pkquery is None:
				
				quey = self.model.objects.filter(Status=True)
				if self.count and self.page:
					paginacion= Paginator(quey,self.count)
					
					if len(paginacion.page(1)) == 0:
						quey = None
					else:
						quey = paginacion.page(self.page)

				if quey is not None:
					total_count = quey.object_list.count()
					f = self.serializer_class(quey, many=True)
					
					
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
					self.MensajeListAdd(mensaje_user =  {'mensaje':'reporte Registrados'}, status="success")
					return Response(self.salida(), status=200)
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'No hay registros'}, status="success")
				return Response(self.salida(), status=200)
			else:
				quey = self.model.objects.filter(Q(pk_publica=self.pkquery)&Q(Status=True)).first()
				if quey is None:
					self.MensajeListAdd(mensaje_user = {'mensaje': 'El reporte no existe'} ,
						mensaje_server = {'mensaje': 'El rol no existe'}, status="success")			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(quey)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

		return Response(self.salida(), status=200)

	def delete(self, request, *arg, **kwargs):
		
		try:
			objeto = self.model.objects.get(Q(pk_publica=self.pkquery)&Q(Status=True))
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = {'mensaje': 'El reporte a sido eliminado exitosamente'})
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e), status="error")
			
		

		return Response(self.salida(), status=200)


	def update(self, request, *arg, **kwargs):


		data = self.get_data_body()
		
		try:
			
			if self.pkquery is None:
				self.MensajeListAdd(mensaje_user= {'mensaje':'Ocurrieron errores al momento de guardar el emailreportes'},
				mensaje_server={'mensaje':'No se a enviado correctamente la variable "pkquery" correspondiente al objeto al cual actualizar en la URL'}, status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
					
					objeto = self.model.objects.get(pk_publica=self.pkquery,
					Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar datos del emailreportes'},
						mensaje_server = {'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'})
					return Response(self.salida(), status=404)
				
				usuarioserializer = self.serializer_class( objeto, data= data,partial=True)

				if usuarioserializer.is_valid():
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user={'mensaje':'emailreportes Actualizado con exito'}, status='success')
					self.JsonAdd(json =  usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el emailreportes'},
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		



class TareaAPI(MonitorMixin, 
            CreateAPIView, 
            ListAPIView, 
            RetrieveAPIView, 
            UpdateAPIView, 
            DestroyAPIView,
            APIView):
	model= tarea
	serializer_class = tareaSerializers

	def post(self, request, *arg, **kwargs):
		""" Recibe los un json con los datos del tarea a registrar
		"""
		data = self.get_data_body()
		dataser = self.serializer_class(data=data)
		if dataser.is_valid():
			# dataser.validated_data['creador'] = self.usuario
			dataser.save()
			self.MensajeListAdd( mensaje_user = {'mensaje':'El tarea se registro con exito'}, status='success')
			self.JsonAdd(dataser.data)
			return Response(self.salida(), status=200)
		else:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No se logro registrar el tarea'}, status='error')
			self.JsonAdd(dataser.errors)
			return Response(self.salida(), status=200)
		
	def get(self, request, *arg, **kwargs):
		""" 
		Por defecto obtiene las tareas asignadas al usuario que realiza la petición.
		Enviar por get "pkquery" con la clave primaria del registro a buscar, el no enviar este valor implica obtener
		  las tareas asignadas al usuario que realiza la petición, de ser asi enviar: \n
					count: numero de elementos por pagina \n
					page: numero de pagina 
		Si quieres obtener las tareas de un proyecto determinado envia:\n
					pk_proyecto: que seria el pk_publica del proyecto en cuestión 		
		
		
		"""
		pk_proyecto = request.GET.get('pk_proyecto')
		try:
			if self.pkquery is None:
				query = self.model.objects.filter(Q(Status=True))
				if pk_proyecto != None:

					quey = self.model.objects.filter(Q(Status=True), Q(proyecto__pk_publica=pk_proyecto))
				else:
					quey = self.model.objects.filter(Q(Status=True), Q(asignado__Correo=self.usuario.email))
				
				if self.count and self.page:
					paginacion= Paginator(quey,self.count)
					
					if len(paginacion.page(1)) == 0:
						quey = None
					else:
						quey = paginacion.page(self.page)

				if quey is not None:
					total_count = quey.object_list.count()
					f = self.serializer_class(quey, many=True)
					
					
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
					self.MensajeListAdd(mensaje_user =  {'mensaje':'Tu lista de tareas'}, status="success")
					return Response(self.salida(), status=200)
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'No hay registros'}, status="success")
				return Response(self.salida(), status=200)
			else:
				quey = self.model.objects.filter(Q(pk_publica=self.pkquery)&Q(Status=True)).first()
				if quey is None:
					self.MensajeListAdd(mensaje_user = {'mensaje': 'El tarea no existe'} ,
						mensaje_server = {'mensaje': 'El tarea no existe'}, status="success")			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(quey)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

		return Response(self.salida(), status=200)

	def delete(self, request, *arg, **kwargs):
		
		try:
			objeto = self.model.objects.get(Q(pk_publica=self.pkquery)&Q(Status=True))
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = {'mensaje': 'El tarea a sido eliminado exitosamente'})
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e), status="error")
			
		

		return Response(self.salida(), status=200)


	def update(self, request, *arg, **kwargs):


		data = self.get_data_body()
		
		try:
			
			if self.pkquery is None:
				self.MensajeListAdd(mensaje_user= {'mensaje':'Ocurrieron errores al momento de guardar el tarea'},
				mensaje_server={'mensaje':'No se a enviado correctamente la variable "pkquery" correspondiente al objeto al cual actualizar en la URL'}, status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
					
					objeto = self.model.objects.get(pk_publica=self.pkquery,
					Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar datos del tarea'},
						mensaje_server = {'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'})
					return Response(self.salida(), status=404)
				
				usuarioserializer = self.serializer_class( objeto, data= data,partial=True)

				if usuarioserializer.is_valid():
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user={'mensaje':'tarea Actualizado con exito'}, status='success')
					self.JsonAdd(json =  usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el tarea'},
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)







class comentarioAPI(MonitorMixin, 
            CreateAPIView, 
            ListAPIView, 
            RetrieveAPIView, 
            UpdateAPIView, 
            DestroyAPIView,
            APIView):
	model= comentario
	serializer_class = comentarioSerializers

	def post(self, request, *arg, **kwargs):
		""" Recibe los un json con los datos del comentario a registrar
		"""
		data = self.get_data_body()
		dataser = self.serializer_class(data=data)
		if dataser.is_valid():
			dataser.validated_data['usuario'] = user.objects.get(pk_publica=self.usuario.pk_publica) 
			dataser.save()
			# dataser.instance.usuario = user.objects.get(pk_publica=self.usuario.pk_publica) 
			# dataser.instance.save()
			self.MensajeListAdd( mensaje_user = {'mensaje':'El comentario se registro con exito'}, status='success')
			self.JsonAdd(dataser.data)
			return Response(self.salida(), status=200)
		else:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No se logro registrar el comentario'}, status='error')
			self.JsonAdd(dataser.errors)
			return Response(self.salida(), status=200)
		
	def get(self, request, *arg, **kwargs):
		
		""" 
		Envia "pk_tarea" por params para obtener los comentarios de una tarea especifica. \n
					count: numero de elementos por pagina \n
					page: numero de pagina """
		try:
			pk_tarea = request.GET.get('pk_tarea')
			if self.pkquery is None:
				if pk_tarea != None:
					quey = self.model.objects.filter(Q(Status=True), Q(tarea__pk_publica=pk_tarea))
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'Ocurrio un error'},mensaje_server={"mensaje":"por favor envia el pk_tarea correspondiente a la tarea" } , status="success")
					return Response(self.salida(), status=200)
					
				if self.count and self.page:
					paginacion= Paginator(quey,self.count)
					
					if len(paginacion.page(1)) == 0:
						quey = None
					else:
						quey = paginacion.page(self.page)

				if quey is not None:
					total_count = quey.object_list.count()
					f = self.serializer_class(quey, many=True)
					
					
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
					self.MensajeListAdd(mensaje_user =  {'mensaje':'Tu lista de comentarios'}, status="success")
					return Response(self.salida(), status=200)
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'No hay registros'}, status="success")
				return Response(self.salida(), status=200)
			else:
				quey = self.model.objects.filter(Q(pk_publica=self.pkquery)&Q(Status=True)).first()
				if quey is None:
					self.MensajeListAdd(mensaje_user = {'mensaje': 'El comentario no existe'} ,
						mensaje_server = {'mensaje': 'El comentario no existe'}, status="success")			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(quey)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

		return Response(self.salida(), status=200)

	def delete(self, request, *arg, **kwargs):
		
		try:
			usuario = self.get_user()
			objeto = self.model.objects.get(Q(pk_publica=self.pkquery),
									Q(usuario=usuario),
									Q(Status=True ))
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = {'mensaje': 'El comentario a sido eliminado exitosamente'})
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e), status="error")
			
		

		return Response(self.salida(), status=200)


	def update(self, request, *arg, **kwargs):
		"""
		Para actualizar enviar por params "pkquery" que corresponde al pk_publica del comentario que deseas actualizar
		"""

		data = self.get_data_body()
		
		try:
			
			if self.pkquery is None:
				self.MensajeListAdd(mensaje_user= {'mensaje':'Ocurrieron errores al momento de guardar el comentario'},
				mensaje_server={'mensaje':'No se a enviado correctamente la variable "pkquery" correspondiente al objeto al cual actualizar en la URL'}, status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
				
					objeto = self.model.objects.get(Q(pk_publica=self.pkquery),
									Q(usuario=usuario),
									Q(Status=True ))
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar datos del comentario'},
						mensaje_server = {'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'}, status="NotFound")
					return Response(self.salida(), status=200)
				
				usuarioserializer = self.serializer_class( objeto, data= data,partial=True)

				if usuarioserializer.is_valid():
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user={'mensaje':'comentario Actualizado con exito'}, status='success')
					self.JsonAdd(json =  usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el comentario'},
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)




