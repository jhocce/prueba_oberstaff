
import os
import jwt
import string
import secrets
import time
from datetime import datetime
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from dateutil import tz
from django.db.models import Q

from apps.system.ManageApi import ErrorManagerMixin
from apps.system.monitor import MonitorMixin
from apps.system.models import login
from .models import user, Token, Contacto, rol
from .serializers import UsuarioSerializer, LoginSerializer, UsuarioPresentacionSerializer
from .serializers import ContactoSerializers, RolSerializers


class AdminUserApi(MonitorMixin, CreateAPIView, ListAPIView, 
	RetrieveAPIView, UpdateAPIView, DestroyAPIView, APIView):
	serializer_class = UsuarioSerializer
	model= user
	def post(self, request, *arg, **kwargs):
		
		
		data = self.get_data_body()
		if 'email' not in data.keys():
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el email', status='error')
			return Response(self.salida(), status=200)

		if 'password' not in data.keys():
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el password', status='error')
			return Response(self.salida(), status=200)
		
		if 'username' not in data.keys():
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el username', status='error')
			return Response(self.salida(), status=200)

		UsuarioSerializerresponse = UsuarioSerializer(data= data) 
		if UsuarioSerializerresponse.is_valid():

			alphabet = string.ascii_letters + string.digits
			code = ''.join(secrets.choice(alphabet) for i in range(8))
			UsuarioSerializerresponse.validated_data['Codigo'] = code
			UsuarioSerializerresponse.validated_data['Nombre_completo'] = ""
			if "Nombres" in UsuarioSerializerresponse.validated_data:
				UsuarioSerializerresponse.validated_data['Nombre_completo'] += UsuarioSerializerresponse.validated_data['Nombres']
			if "Apellidos" in UsuarioSerializerresponse.validated_data:
				UsuarioSerializerresponse.validated_data['Nombre_completo'] += UsuarioSerializerresponse.validated_data['Apellidos']
			# try:
			# 	UsuarioSerializerresponse.validated_data['Nombre_completo'] = lambda x: UsuarioSerializerresponse.validated_data['Nombres'] != None  + UsuarioSerializerresponse.validated_data['Apellidos']
			# except Exception as e:
			# 	pass
			toke = Token.objects.create(user=UsuarioSerializerresponse.instance)
			toke.save()
			UsuarioSerializerresponse.save()
			self.JsonAdd(json={
				"pk_publica":UsuarioSerializerresponse.data['pk_publica'],
				"Nombres":UsuarioSerializerresponse.data['Nombres'],
				"Apellidos":UsuarioSerializerresponse.data['Apellidos'],
				"username":UsuarioSerializerresponse.data['username'],
				"rol":UsuarioSerializerresponse.data['rol'],
				"Contacto":UsuarioSerializerresponse.data['Contacto'],
				# "tokenUser": jwt.encode({'pk_publica': str(UsuarioSerializerresponse.data['pk_publica']), 'session':str(toke.pk_publica)}, settings.SECRET_KEY_USER , algorithm="HS256")


			})
			self.MensajeListAdd( mensaje_user = {'mensaje':'Ahora puedes iniciar sesión'}, 
						mensaje_server=UsuarioSerializerresponse.errors, status='success')

			return Response(self.salida(), status=200)
		else:
			
			self.MensajeListAdd( mensaje_user = UsuarioSerializerresponse.errors, 
						mensaje_server=UsuarioSerializerresponse.errors, status='error')
			return Response(self.salida(), status=200)
	
	def get(self, request, *arg, **kwargs):
		""" Enviar por get "pkquery" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
				de todos los registros del usuario en cuestion de ser asi enviar: \n
					count: numero de elementos por pagina \n
					page: numero de pagina """
		try:
			
			if self.pkquery is None:
				# self.criterios="Tipo=Admin"
				user1 = self.get_user()
				if user1.is_superuser:
					query =  self.model.objects.filter(Status=True)
					# quey = self.get_queryset()
					if query is not None:
						total_count = query.count()
						if self.count and self.page:
							
							paginacion= Paginator(query,self.count)
							
							if len(paginacion.page(1)) == 0:
								pass
							else:
								query = paginacion.page(self.page)
						
						
						f = self.serializer_class(query, many=True)
						data = []
						for a in f.data:
							a['password'] = "**********************"
							data.append(a)
						
						self.JsonAdd(json={
							"total_count":total_count,
							"data":data
							})
						self.MensajeListAdd(mensaje_user =  {'mensaje':'usuarios registrados'}, status="success")
					else:
						self.MensajeListAdd(mensaje_user = 'No hay registros')
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'El usuario no tiene permisos suficientes'}, status="denied")
				return Response(self.salida(), status=200)
			else:
				
				
				try:
					query= self.model.objects.get(pk_publica=self.pkquery)
					f = UsuarioPresentacionSerializer(query)
					self.JsonAdd(json=f.data)
					self.MensajeListAdd(mensaje_user ={'mensaje':'usuarios registrados'}, status="success")
					return Response(self.salida(), status=200)
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = 'El Usuario no existe',
						mensaje_server = 'El Usuario no existe o no pertenece al usuario relacionado con el token')			
					return Response(self.salida(), status=200)
			
					

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

	def delete(self, request, *arg, **kwargs):
		
		# self.data_body=request.data
		# self.data_body = self.get_data_body()
		try:
			objeto = self.model.objects.get(pk_publica=self.pkquery)
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = {"mensaje": "El usuario a sido eliminado exitosamente"}, status="success")
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e), status="error")

		return Response(self.salida(), status=200)
	
	def update(self, request, *arg, **kwargs):


		data = self.get_data_body()
		
		try:
			
			if self.pkquery is None:
				self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el Usuario'},
				mensaje_server={'mensaje':'No se a enviado correctamente la variable "pk" correspondiente al objeto al cual actualizar en la URL'}, status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
					
					objeto = self.model.objects.get(pk_publica=self.pkquery,
					Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar el Usuario'},
						mensaje_server ={'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'})
					return Response(self.salida(), status=404)
				
				usuarioserializer = UsuarioPresentacionSerializer( objeto, data= data,partial=True)

				if usuarioserializer.is_valid():
					
					try:
						usuarioserializer.validated_data['password'] = usuarioserializer.validated_data['password']
					except Exception as e:
						pass
					
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user={'mensaje': 'Usuario guardado con exito'}, status='success')
					se = usuarioserializer.data
					
					self.JsonAdd(json =  usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user={'mensaje': 'Ocurrieron errores al momento de guardar el Usuario'},
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

	def __str__(self):
		return "AdminUserApi"



class LogoutUserApi(MonitorMixin, ErrorManagerMixin, APIView):
	

	def get(self, request, *arg, **kwargs):
		""" Obtiene los datos que corresponden al token """
		try:
				
			tokenJWTENCODE = request.headers.get('Authorization', '').replace('Bearer', '').strip()
			tokenJWTDECODE = jwt.decode(tokenJWTENCODE, settings.SECRET_KEY_TOKEN , algorithms="HS256")
			token = tokenJWTDECODE['token']
			utc = tz.tzutc()
			local = tz.tzlocal()
			token = Token.objects.get(token=token)
			
			fecha2 = datetime.now()

			ultima_peticion = str(token.Modificado)
			fecha1 = token.Modificado.replace(tzinfo=utc)
			fecha1 = fecha1.astimezone(local)

			diferencia = time.mktime(fecha2.timetuple()) - time.mktime(fecha1.timetuple()) 

			if diferencia > (60*60*6):

				self.MensajeListAdd( mensaje_user = 'Su sesion a expirado')
				token.Status = False
				token.save()
				
			else:
				token.Modificado = datetime.now()
				token.save()
				permisos = token.user.Tipo

				self.JsonAdd(json = {
					'ambito': permisos,
					'ultima_peticion':ultima_peticion,
					'Status': token.Status,
					'usuario': token.user.username,
					})
		except Exception as e:
			self.MensajeListAdd( mensaje_user = 'No autorizado',
				mensaje_server="No autorizado",
				status= 303)
			# print(request.session.keys())
			# print(self.salida())
			# return False
		return Response(self.salida(), status=200)
	def post(self, request, *arg, **kwargs):
		""" Cierra sesion del token que has pasado """
		# token = request.data['token']
		tokenJWTENCODE = request.headers.get('Authorization', '').replace('Bearer', '').strip()
		tokenJWTDECODE = jwt.decode(tokenJWTENCODE, settings.SECRET_KEY_TOKEN , algorithms="HS256")
		token = tokenJWTDECODE['token']

		try:
			token = Token.objects.get(token=token)
			token.Status = False
			token.save()
			self.MensajeListAdd(mensaje_user = 'Sesion finalizada')

		except Exception as e:
			self.MensajeListAdd( mensaje_server = str(e))
			return Response(self.salida(), status=404)
		
		return Response(self.salida(), status=200)


class LoginUserAPI( ErrorManagerMixin,CreateAPIView, APIView):
	
	
	serializer_class = LoginSerializer
	model = login
	def get_data_body(self):
		LOCATION_KEYS_PRIVATE = os.environ.get("LOCATION_KEYS_PRIVATE")
		
		with open(LOCATION_KEYS_PRIVATE + "/private_back.pem", "rb") as f:
			private_key = f.read()
		if self.jwt:
			dat = jwt.decode(self.data_body, private_key , algorithms="RS256")
			return dat
		else:
			return self.data_body
	def post(self, request, *arg, **kwargs):
		"""DDDDDDDDDDDD"""
		self.data_body=request.data
	
		data = self.get_data_body()
		e = ''
		print(data)
		try:
			
			if  'email' not in data.keys():
				self.MensajeListAdd( mensaje_user = {'mensaje':'No estas enviando correctamente el email'}, 
								 status='error')
				return Response(self.salida(), status=500)

			if  'password' not in data.keys():
				self.MensajeListAdd( mensaje_user = {'mensaje':'No estas enviando correctamente el password'}, 
								 status='error')
				return Response(self.salida(), status=500)
		except Exception as e:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No estas enviando correctamente el passsword y username'}, 
								 status='error')
			return Response(self.salida(), status=500)
		
		email =  data['email']
		password =  data['password']
		
		try:
			usermodel = user.objects.filter(Q(email=email)&Q(password=password))
			usuario = usermodel.first()
			if usermodel.count() == 0:
				self.MensajeListAdd(mensaje_user =  {'mensaje':'Usuario o contraseña invalida'}, status='not_auth')
				return Response(self.salida(), status=200)
			else:
				try:
					tokens = Token.objects.filter(user =  usuario, Status=True)
					for tok in tokens:
						tok.Status = False
						tok.save()

				except Exception as e:
				
					self.MensajeListAdd(mensaje_server  = str(e))
					return Response(self.salida(), status=500)

					
				token = Token(user = usuario)
				token.save()
				encoded = jwt.encode({'pk_publica': str(usuario.pk_publica), 'session':str(token.token)}, settings.SECRET_KEY_USER , algorithm="HS256")
				
				jsonresp = {
					'token' : encoded
				}
				self.MensajeListAdd(mensaje_user = {'mensaje':'iniciando sesion'}, status='success')
				self.JsonAdd(json=jsonresp)
				
		
				return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd( mensaje_server = str(e))
			return Response(self.salida(), status=500)
			
		
	def __str__(self):
		return 'LoginUserAPI'





class RolAPI(MonitorMixin, 
            # CreateAPIView, 
            ListAPIView, 
            # RetrieveAPIView, 
            # UpdateAPIView, 
            # DestroyAPIView,
            APIView):
	model= rol
	serializer_class = RolSerializers

	# def post(self, request, *arg, **kwargs):
	# 	""" Recibe los un json con los datos del rol a registrar
	# 	"""
	# 	data = self.get_data_body()
	# 	dataser = self.serializer_class(data=data)
	# 	if dataser.is_valid():
	# 		# dataser.validated_data['user'] = self.usuario
	# 		dataser.save()
	# 		self.MensajeListAdd( mensaje_user = {'mensaje':'El rol se registro con exito'}, status='success')
	# 		self.JsonAdd(dataser.data)
	# 		return Response(self.salida(), status=200)
	# 	else:
	# 		self.MensajeListAdd( mensaje_user = {'mensaje':'No se logro registrar el rol'}, status='error')
	# 		self.JsonAdd(dataser.errors)
	# 		return Response(self.salida(), status=200)
		
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
					self.MensajeListAdd(mensaje_user =  {'mensaje':'Roles Registrados'}, status="success")
					return Response(self.salida(), status=200)
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'No hay registros'}, status="success")
				return Response(self.salida(), status=200)
			else:
				quey = self.model.objects.filter(Q(pk_publica=self.pkquery)&Q(Status=True)).first()
				if quey is None:
					self.MensajeListAdd(mensaje_user = {'mensaje': 'El rol no existe'} ,
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

	# def delete(self, request, *arg, **kwargs):
		
	# 	try:
	# 		objeto = self.model.objects.get(Q(pk_publica=self.pkquery)&Q(Status=True))
	# 		objeto.Status = False
	# 		objeto.save()
	# 		self.MensajeListAdd(mensaje_user = {'mensaje': 'El rol a sido eliminado exitosamente'})
	# 	except Exception as e:
	# 		self.MensajeListAdd(mensaje_server  = str(e), status="error")
			
		

	# 	return Response(self.salida(), status=200)


	# def update(self, request, *arg, **kwargs):


	# 	data = self.get_data_body()
		
	# 	try:
			
	# 		if self.pkquery is None:
	# 			self.MensajeListAdd(mensaje_user= {'mensaje':'Ocurrieron errores al momento de guardar el rol'},
	# 			mensaje_server={'mensaje':'No se a enviado correctamente la variable "pk" correspondiente al objeto al cual actualizar en la URL'}, status='error')
	# 			return Response(self.salida(), status=303)
	# 		else:
	# 			try:
	# 				usuario = self.get_user()
					
	# 				objeto = self.model.objects.get(pk_publica=self.pkquery,
	# 				Status=True )
	# 			except self.model.DoesNotExist:
	# 				self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar datos del rol'},
	# 					mensaje_server = {'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'})
	# 				return Response(self.salida(), status=404)
				
	# 			usuarioserializer = self.serializer_class( objeto, data= data,partial=True)

	# 			if usuarioserializer.is_valid():
	# 				usuarioserializer.save()
	# 				self.MensajeListAdd(mensaje_user={'mensaje':'rol Actualizado con exito'}, status='success')
	# 				self.JsonAdd(json =  usuarioserializer.data )
	# 				return Response( self.salida(), status=200)
	# 			else:
	# 				self.JsonAdd(json = usuarioserializer.errors )
	# 				self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el rol'},
	# 					mensaje_server=usuarioserializer.errors, status='error')

	# 				return Response(self.salida(), status=200)
	# 	except Exception as e:
	# 		self.MensajeListAdd(mensaje_server  = str(e))
	# 		return Response(self.salida(), status=500)
		






class ContactoAPI(MonitorMixin, 
            CreateAPIView, 
            ListAPIView, 
            RetrieveAPIView, 
            UpdateAPIView, 
            DestroyAPIView,
            APIView):
	model= Contacto
	serializer_class = ContactoSerializers

	def post(self, request, *arg, **kwargs):
		""" Recibe los un json con los datos del Contacto a registrar
		"""
		data = self.get_data_body()
		dataser = self.serializer_class(data=data)
		if dataser.is_valid():
			dataser.validated_data['ref'] = self.usuario
			dataser.save()
			self.MensajeListAdd( mensaje_user = {'mensaje':'El Contacto se registro con exito'}, status='success')
			self.JsonAdd(dataser.data)
			return Response(self.salida(), status=200)
		else:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No se logro registrar el Contacto'}, status='error')
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
					self.MensajeListAdd(mensaje_user =  {'mensaje':'Contactoes Registrados'}, status="success")
					return Response(self.salida(), status=200)
				else:
					self.MensajeListAdd(mensaje_user =  {'mensaje':'No hay registros'}, status="success")
				return Response(self.salida(), status=200)
			else:
				quey = self.model.objects.filter(Q(pk_publica=self.pkquery)&Q(Status=True)).first()
				if quey is None:
					self.MensajeListAdd(mensaje_user = {'mensaje': 'El Contacto no existe'} ,
						mensaje_server = {'mensaje': 'El Contacto no existe'}, status="success")			
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
			self.MensajeListAdd(mensaje_user = {'mensaje': 'El Contacto a sido eliminado exitosamente'})
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e), status="error")
			
		

		return Response(self.salida(), status=200)


	def update(self, request, *arg, **kwargs):


		data = self.get_data_body()
		
		try:
			
			if self.pkquery is None:
				self.MensajeListAdd(mensaje_user= {'mensaje':'Ocurrieron errores al momento de guardar el Contacto'},
				mensaje_server={'mensaje':'No se a enviado correctamente la variable "pk" correspondiente al objeto al cual actualizar en la URL'}, status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
					
					objeto = self.model.objects.get(pk_publica=self.pkquery,
					Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = {'mensaje':'Ocurrieron uno o mas errores a actualizar datos del Contacto'},
						mensaje_server = {'mensaje':'El objeto no existe o no pertenece al usuario al que esta relacionado al token'})
					return Response(self.salida(), status=404)
				
				usuarioserializer = self.serializer_class( objeto, data= data,partial=True)

				if usuarioserializer.is_valid():
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user={'mensaje':'Contacto Actualizado con exito'}, status='success')
					self.JsonAdd(json =  usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user={'mensaje':'Ocurrieron errores al momento de guardar el Contacto'},
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		



