import logging
from apps.user.models import rol, user
from rest_framework.test import APITestCase

logger = logging.getLogger('tests')

class loginTestClass(APITestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        
        # Asegurar que hay al menos un handler
        if not logger.handlers:
            logger.addHandler(logging.StreamHandler())
        logger.info("Obteniendo nuevo token con usuario de pruebas .......")
      
        response = self.client.post("/user/login/", format='json',  data={
                "email":"prueba@prueba.com",
                "password":"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["entity"], "login")
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "iniciando sesion"}])
        self.token_access = response.data["json"][0]["token"]
        
        logger.debug("OK")
        response = self.client.get('/user/rol/' ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["entity"], "rol")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "Roles Registrados"}])
        self.assertIsInstance(response.data["json"], list)
        json_rol = response.data["json"][0]['data']
        self.roles = json_rol
        pass

    def tearDown(self):
       
        logger.debug("Limpiando data de prueba.... ")
        # print("Eliminando servidor de testing ..................", end=" ")
        # servidor.objects.get(Nombre="testing").delete()
        logger.debug("OK")

        pass

    def test_obtener_rol(self):
        roles = rol.objects.filter(Status=True)
        logger.debug("revisando roles de data migrada...")
        
        self.assertEqual(roles.count(), 4 )
        logger.debug("Roles obtenidos:  {0}/3".format(roles.count()))

        logger.debug("OK....")

    def test_usuario_1_rolDataEntry_testAuto(self):

        logger.debug("Registrar usuario de pruebas automatizadas ...................")
        data={
            "username":"pruebatest1",
            "email":"pagina1@hot.com",
            "password":"123456",
            "rol":next((item["pk_publica"] for item in self.roles if item["Nombre"] == "Administrador"), None)
        }
        response = self.client.post('/user/', data = data ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "user")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "Ahora puedes iniciar sesión"}])
        self.assertEqual(response.data["json"][0]['username'],data['username'] ) 
        # self.assertEqual(response.data["json"][0]['rol']['Nombre'],'Data Entry' ) 
        pk_user = response.data["json"][0]['pk_publica']
        logger.debug("OK")
        logger.debug("Actualizando usuario de pruebas automatizadas ...................")
        data={
            "pk_publica": pk_user,
            "Nombres":"actuzalizado"
        }
        response = self.client.put('/user/', data = data, query_params={"pkquery":pk_user} ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "user")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "Usuario guardado con exito"}])
        user_put=response.data["json"][0]
        self.assertEqual(user_put["Nombres"], data["Nombres"])
        logger.debug("OK")
        logger.debug("Evaluando obtener usuarios.............")
        response = self.client.get('/user/' ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "denied")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "user")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "El usuario no tiene permisos suficientes"}])
        self.assertIsInstance(response.data["json"], list)
        logger.debug("OK")
        logger.debug("Eliminar usuario de prueba......................")
        response = self.client.delete('/user/', query_params={"pkquery":pk_user} ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "user")
        self.assertIn("menssage_user", response.data)
      
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "El usuario a sido eliminado exitosamente"}])
        logger.debug("OK")


    # def test_contactos(self):
        

    #     logger.debug("Registrar contacto de pruebas automatizadas ...................")
    #     data={
    #         "Nombre":"prueba",
    #         "Descripcion":"descripsion prueba",
    #         "Estado":
    #     }
    #     response = self.client.post('/user/rol/', data = data ,format='json', headers={ 'Authorization':self.token_access})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("status", response.data)
    #     self.assertEqual(response.data["status"], "success")
    #     self.assertIn("entity", response.data)
    #     self.assertEqual(response.data["entity"], "rol")
    #     self.assertIn("menssage_user", response.data)
    #     self.assertEqual(response.data["menssage_user"], [{"mensaje": "El rol se registro con exito"}])
    #     self.assertEqual(response.data["json"][0]['Nombre'],data['Nombre'] ) 
    #     pk_user = response.data["json"][0]['pk_publica']
    #     logger.debug("OK")
    #     logger.debug("Actualizando usuario de pruebas automatizadas ...................")
    #     data={
    #         "pk_publica": pk_user,
    #         "Nombre":"actuzalizado"
    #     }
    #     response = self.client.put('/user/rol/', data = data ,format='json',query_params={"pkquery":pk_user} , headers={ 'Authorization':self.token_access})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("status", response.data)
    #     self.assertEqual(response.data["status"], "success")
    #     self.assertIn("entity", response.data)
    #     self.assertEqual(response.data["entity"], "rol")
    #     self.assertIn("menssage_user", response.data)
    #     self.assertEqual(response.data["menssage_user"], [{"mensaje": "rol Actualizado con exito"}])
    #     user_put=response.data["json"][0]
    #     self.assertEqual(user_put["Nombre"], data["Nombre"])
    #     logger.debug("OK")
    #     logger.debug("Evaluando obtener usuarios.............")

    #     response = self.client.get('/user/rol/' ,format='json', headers={ 'Authorization':self.token_access})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("status", response.data)
    #     self.assertEqual(response.data["status"], "success")
    #     self.assertIn("entity", response.data)
    #     self.assertEqual(response.data["entity"], "rol")
    #     self.assertIn("menssage_user", response.data)
    #     self.assertEqual(response.data["menssage_user"], [{"mensaje": "Roles Registrados"}])
    #     self.assertIsInstance(response.data["json"], list)
    #     logger.debug("OK")
    #     logger.debug("Eliminar usuario de prueba......................")
    #     response = self.client.delete('/user/rol/', query_params={"pkquery":pk_user} ,format='json', headers={ 'Authorization':self.token_access})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("status", response.data)
    #     self.assertEqual(response.data["status"], "success")
    #     self.assertIn("entity", response.data)
    #     self.assertEqual(response.data["entity"], "rol")
    #     self.assertIn("menssage_user", response.data)
    #     self.assertEqual(response.data["menssage_user"], [{"mensaje": "El rol a sido eliminado exitosamente"}])
    #     logger.debug("OK")

    def test_proyecto_1_testAuto(self):

        logger.debug("Registrar proyecto de pruebas automatizadas ...................")
        datapost={
            'Nombre':'prueba',
            'Descripcion':"pruebas"
        }
       
        response = self.client.post('/proyecto/', data = datapost, format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
     
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "Proyecto")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "El proyecto se registro con exito"}])
        
        self.assertEqual(response.data["json"][0]['Nombre'],datapost['Nombre'] ) 
        pk_proyecto = response.data["json"][0]['pk_publica']
        logger.debug("OK")
        logger.debug("insertando correos para alerta en el proyecto ...................")


        data_email={
           
            "email":[
                "prueba@prueba.com",
            ],
            "proyecto":pk_proyecto
        }
        response = self.client.post('/proyecto/emailreportes', data = data_email, format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
     
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "emailreportes")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "El reporte se registro con exito"}])

        logger.debug("Actualizando proyecto de pruebas automatizadas ...................")

        data={
            "pk_publica": pk_proyecto,
            "Descripcion":"actuzalizado"
        }
        response = self.client.put('/proyecto/', data = data, query_params={"pkquery":pk_proyecto} ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "Proyecto")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "proyecto Actualizado con exito"}])
        proyecto_put=response.data["json"][0]
        self.assertEqual(proyecto_put["Nombre"], datapost["Nombre"])

        logger.debug("OK")
        logger.debug("Evaluando obtener proyectos.............")

        response = self.client.get('/proyecto/' ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "Proyecto")
        self.assertIn("menssage_user", response.data)
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "El proyecto se registro con exito"}])
        self.assertIsInstance(response.data["json"], list)
        
        logger.debug("OK")
        logger.debug("Eliminar proyecto de prueba......................")

        response = self.client.delete('/proyecto/', query_params={"pkquery":pk_proyecto} ,format='json', headers={ 'Authorization':self.token_access})
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("entity", response.data)
        self.assertEqual(response.data["entity"], "Proyecto")
        self.assertIn("menssage_user", response.data)
      
        self.assertEqual(response.data["menssage_user"], [{"mensaje": "El proyecto a sido eliminado exitosamente"}])




# 'Nombre','Descripcion','FechaDeInicio','Reportemail', 'AlertaDiaria', 'AlertaSemanal', 'TormentaDeAlerta'