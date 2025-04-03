import os
import json
import requests
import flet as ft
from  datetime import datetime
from dateutil.parser import parse

class ModifiedResponse:
    def __init__(self, original_response, new_data):
        self.status_code = original_response.status_code
        self.headers = original_response.headers
        self._content = json.dumps(new_data).encode('utf-8')
    
    def json(self):
        return json.loads(self._content)
    
    
class request():

    def __init__(self):
        # self.page=page
        pass
    def handle_action_click(self, e):
        self.page.close(e.control.parent)
        pass
    def Get(self, url, headers=None, **kwargs):
        tokenkey = self.page.session.get("tokenkey")
  
        headers =  {'Authorization': 'Bearer {0}'.format(tokenkey), "Content-Type":"application/json"}     
        
        respuesta = requests.get(url=os.environ.get("ulr_api")+url, headers=headers, **kwargs)

        if respuesta.json()['status']=="success":
            key = "prueba.cache.{0}".format(respuesta.json()['entity'])
            
            if self.page.client_storage.contains_key(key):
                cuerpo = self.page.client_storage.get(key)
                if (datetime.now()-parse(cuerpo['fecha'])).total_seconds() >= 300:
           
                    self.page.client_storage.set(key, {
                        "fecha":str(datetime.now()),
                        "content":respuesta.json()['json'][0]
                    })
                else:
                    res = respuesta.json()
                    res['json'][0]=cuerpo['content']
                    modified_response = ModifiedResponse(respuesta, res)
                    # res.status_code = respuesta.status_code
                    return modified_response
            else:
                self.page.client_storage.set(key, {
                        "fecha":str(datetime.now()),
                        "content":respuesta.json()['json'][0]
                    })
        return respuesta
    def Post(self, url, headers=None, data=None, **kwargs):
        tokenkey = self.page.session.get("tokenkey")
  
        headers =  {'Authorization': 'Bearer {0}'.format(tokenkey), "Content-Type":"application/json"}
        respuesta = requests.post(url=os.environ.get("ulr_api")+url, headers=headers, data = json.dumps(data), **kwargs)
       
        if respuesta.json()['status']=="success":
            key = "prueba.cache.{0}".format(respuesta.json()['entity'])
            if self.page.client_storage.contains_key(key):
                self.page.client_storage.remove(key)
        return respuesta
    def Update(self, url, headers=None, data=None, **kwargs):
        tokenkey = self.page.session.get("tokenkey")
  
        headers =  {'Authorization': 'Bearer {0}'.format(tokenkey), "Content-Type":"application/json"}
        respuesta = requests.put(url=os.environ.get("ulr_api")+url, headers=headers, data = json.dumps(data), **kwargs)
       
        if respuesta.json()['status']=="success":
            key = "prueba.cache.{0}".format(respuesta.json()['entity'])
            if self.page.client_storage.contains_key(key):
                self.page.client_storage.remove(key)
        return respuesta
    def Delete(self, url, headers=None, data=None, **kwargs):
        tokenkey = self.page.session.get("tokenkey")
  
        headers =  {'Authorization': 'Bearer {0}'.format(tokenkey), "Content-Type":"application/json"}
        respuesta = requests.delete(url=os.environ.get("ulr_api")+url, headers=headers, data = json.dumps(data), **kwargs)
       
        if respuesta.json()['status']=="success":
            key = "prueba.cache.{0}".format(respuesta.json()['entity'])
            if self.page.client_storage.contains_key(key):
                self.page.client_storage.remove(key)
        return respuesta