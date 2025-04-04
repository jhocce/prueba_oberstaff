import os
import jwt



with open(os.environ.get("LOCATION_KEYS_PRIVATE") + "/private_back.pem", "rb") as f:
	public_key = f.read()
class ErrorManagerMixin():
	""" Clase que maneja la estructura y control de las salidas de errores
	de la forma: 
	{
		'status': '',
			'operacion':'',
			'entidad':'',
			'mensaje_user':[],
			'mensaje_server':[],
			'json' : []
	}
	operacion: 	Nombre de la operacion al momento de generarse la llamada
	entidad: refiere al modelo sobre el cual se estaba trabajando al generarse
		la llamada
	mensaje_user: con tiene un array de cadenas con los mensajes que se le 
		presentaran al usuario
	mensaje_server: mensaje comunmente de error que sera expresado para 
		darle a saber al desarrollador frontend de un error en la peticion  
	status: el estado de la peticion dentro del servidor para el usuario
		indiferente del	estado de la peticion que se encuentra en las cabeceras
		de la peticion, su razon es servir como controlador de mensajes para el
		usuario
	 """
	def __init__(self):
		self.jwt=False
		
		self.responseapi={
			'status': '',
			'operation':'',
			'entity':'',
			'menssage_user':[],
			'menssage_server':[],
			'json' : []
		}
		self.errorMixin = False
		return super(ErrorManagerMixin, self).__init__()
	def GetModel(self):
		""" Obtiene el modelo de la vista donde es heredado """
		return self.model
	def JsonAdd(self, json):
		""" A;ade la respuesta Json en el cuerpo de la respuesta """
		self.responseapi['json'].append(json)

	def MensajeListAdd(self, mensaje_user='', 
						mensaje_server='', 
						status='success'):
		""" A;ande un error a la lista de errores. """
		self.errorMixin = True
		self.responseapi['status'] = status
		if mensaje_user!='':
			self.responseapi['menssage_user'].append(mensaje_user)
		if mensaje_server!='':
			self.responseapi['menssage_server'].append(mensaje_server)
	def MensajeList(self):
		""" retorna la respuesta con los errores capturados al 
		momento de ser invocada """
		try:
			name_model = self.GetModel().__name__
		except Exception as e:
			name_model = "Security"
		if self.errorMixin:
			self.responseapi['operation'] = str(self.__class__())
			self.responseapi['entity'] = name_model
		else:
			self.responseapi['operation'] = str(self.__class__())
			self.responseapi['entity'] = name_model
		
		return self.responseapi

	def salida(self):
		"""Retorna la salida del mensaje en formato json"""
		
		if self.jwt:
			return "{0}".format(jwt.encode(self.MensajeList(), public_key, algorithm="RS256")) 
		else:
			return self.MensajeList()
		
