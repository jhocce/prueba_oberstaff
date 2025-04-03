import jwt
import uuid 
import time
import json
from django.apps import apps
from django.conf import settings
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q, F
from apps.system.ManageApi import ErrorManagerMixin
from datetime import datetime
from apps.user.models import user, Token
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from dateutil import tz
from ast import literal_eval
class ErrorMonitor(Exception):
    pass





class MonitorMixin(ErrorManagerMixin):
	""" Clase que hereda de ErrorManagerMixin y es encargada de
		monitorear y controlar los accesos del usuario a las 
		peticiones al sistema

	  """
	estado = False
	def dispatch(self, request, *args, **kwargs):
		if "Authorization" not in request.headers:
			self.MensajeListAdd( mensaje_user = {'mensaje':'Error!'},
					mensaje_server="No has enviado el campo Authorization en l header",
					status= "error")
			
			return HttpResponse( json.dumps(self.salida()) , status=303)
		
		tokenJWTENCODE = request.headers.get('Authorization', '').replace('Bearer', '').strip()
		tokenJWTDECODE = jwt.decode(tokenJWTENCODE, settings.SECRET_KEY_USER , algorithms="HS256")
		pk_publica = tokenJWTDECODE['pk_publica']
		self.session = tokenJWTDECODE['session']
		self.pkquery = request.GET.get('pkquery')
		# self.token = tokenJWTDECODE['session']
		try:
			self.usuario = user.objects.get(pk_publica=pk_publica)
			self.pk_publica = self.usuario.pk_publica
			# if self.usuario.rol.Nombre != "Admin":
			# 	self.MensajeListAdd( mensaje_user = {'mensaje':'El usuario carece de los permisos adecuados'},
			# 		status= "error")
			# 	print("sadsdasd",self.salida() )

			# 	return HttpResponse( json.dumps(self.salida()) , status=303)
	
		except Exception as e:
			print(str(e))
			self.MensajeListAdd( mensaje_user = {'mensaje':'Error!'},
					mensaje_server=str(e),
					status= "error")
			
			return HttpResponse( json.dumps(self.salida()) , status=303)
		self.count = request.GET.get('count')
		
		self.page = request.GET.get('page')
		print(request.body)
		if request.method == "POST" or request.method == "UPDATE"or request.method == "PUT"  or request.method == "PATCH":
			self.data_body = literal_eval(request.body.decode())
		if self.count==None:
			self.count=100
		if self.page==None:
			self.page=1
		self.criterios = request.GET.get('filter')
		if self.__str__() != 'AdminUserApi' and request.method != 'POST':

			if self.valid_token(request=request) is False :
				return HttpResponse( json.dumps(self.salida()) , status=303)
		return super(MonitorMixin, self).dispatch(request,*args, **kwargs )
	def get_data_body(self):
		
		if self.jwt:
			with open(settings.PUBLIC_BACK_URL, "rb") as f:
				private_key = f.read()
			dat = jwt.decode(self.data_body, private_key , algorithms="RS256")
			return dat
		else:
			return self.data_body
	def valid_token(self, request):

		try:			
			utc = tz.tzutc()
			local = tz.tzlocal()
			try:
				
				token = Token.objects.get(token=self.session, Status=True)
			except Exception as e:
				logout(request)
				self.MensajeListAdd( mensaje_user = {'mensaje':'Careces de permisos para esta acción'},
					mensaje_server=str(e),
					status= "error1233")

				return False
				
			  
			fecha2 = datetime.now()
			fecha1 = token.Modificado.replace(tzinfo=utc)
			fecha1 = fecha1.astimezone(local)
			diferencia = time.mktime(fecha2.timetuple()) - time.mktime(fecha1.timetuple()) 
			if diferencia > (60*60*24):
				self.MensajeListAdd( mensaje_user = {'mensaje':'Su sesión a expirado'}, status="sessionout")
				token.Status = False
				token.save()
				return False
			else:
				token.Modificado = datetime.now()
				token.save()
				return True
				
		except Exception as e:
			print(e)
			self.MensajeListAdd( mensaje_server = str(e), status=500)

			return False

	def detallestoken(self, token):

		try:
			# print(token)
			utc = tz.tzutc()
			local = tz.tzlocal()
			token = Token.objects.get(token=token)
			
			fecha2 = datetime.now()

			ultima_peticion = str(token.Modificado)
			fecha1 = token.Modificado.replace(tzinfo=utc)
			fecha1 = fecha1.astimezone(local)

			diferencia = time.mktime(fecha2.timetuple()) - time.mktime(fecha1.timetuple()) 

			if diferencia > (60*60):

				self.MensajeListAdd( mensaje_user = {'mensaje':'Su sesión a expirado'} )
				token.Status = False
				token.save()
				return False
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

				return False
		except Exception as e:
			# print(e)
			self.MensajeListAdd( mensaje_server = str(e), status="error")
			return False

	


	def get_object(self):
		try:
			objeto = self.model.objects.filter(Q(pk_publica=self.pk_publica)&Q(user=self.usuario)&Q(Status=True)).first()
			return objeto
		except Exception as e:
			raise e

	def get_user(self):
		return self.usuario
	def get_queryset(self):
		if self.criterios != None:
			query =  self.model.objects.filter(Q(user=self.usuario)&Q(Status=True))
			campos = self.model._meta.get_fields()

			models = {
			    model.__name__: model for model in apps.get_models()
			}
			campos = [Fila.name for Fila in campos]
			campos.remove('user')
			print(campos)
			condiciones = ''
			lis = []
			argdict = json.loads(self.criterios.encode('utf-8'))
			for x in argdict.keys():
				if "_" in x:
					print(x)
					modelo = x.split("_")[0]
					print(modelo)
					print(models.keys())
					if modelo in models.keys():
						print(argdict[x])
						# print("modelo capturado")
						p = models[modelo].objects.get(pk_publica=argdict[x])
						print("---------------------")
						print(p.id.value_to_string)
						print(dir(p.id))
						if modelo in campos:
							campos.remove(modelo)
							if condiciones != '':
								condiciones = condiciones + 'and ("{0}"={1})'.format(x, p.id )
							else:
								condiciones = condiciones + '("{0}"={1})'.format(x, p.id )
							lis.append(x)
			for modelo in lis:
				del argdict[x]
			i = 0
			for x in argdict.keys():
				i = i+1
				if x in campos:
					if i >1:
						condiciones = condiciones + " and ({0}='{1}')".format(x, argdict[x])
					else:
						condiciones = condiciones + "({0}='{1}')".format(x, argdict[x])
				else:
					raise Exception('El criterio "{0}" enviado en la peticion no se encuentra en estos registros'.format(x))
			sql = 'SELECT * FROM {0}_{1} WHERE {2}'.format(self.model._meta.app_label, self.model._meta.model_name, condiciones)
			print(sql)
			try:
				# print(sql)
				q = query.raw(sql)

			except Exception as e:
				
				raise Exception('Error desconocido: {0} '.format(e))

			return q
		else:
			con = self.model.objects.filter(Q(user=self.usuario)&Q(Status=True))

			if self.count and self.page:
				paginacion= Paginator(con,self.count)
				
				if len(paginacion.page(1)) == 0:
					return None
				else:
					con= paginacion.page(self.page)
			return con
		

	def	get_querysetall(self):
		return self.model.objects.filter(Status=True)
	def get_objectabsolute(self):
		try:
			objeto = self.model.objects.filter(Q(pk_publica=self.pk_publica)&Q(Status=True)).first()
			return objeto
		except Exception as e:
			raise e





