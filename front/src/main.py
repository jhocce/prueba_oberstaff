import os
import flet as ft
import requests
from flet_core.control import Control
from dotenv import load_dotenv
import json
import base64
import hashlib
import secrets

from componets.ui import base
from util.MonitorMixin import MonitorAlert


ALGORITHM = "pbkdf2_sha256"


def hash_password(password, salt=None, iterations=870000):
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return "{}${}${}${}".format(ALGORITHM, iterations, salt, b64_hash)

def verify_password(password, password_hash):
    if (password_hash or "").count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = password_hash.split("$", 3)
    iterations = int(iterations)
    assert algorithm == ALGORITHM
    compare_hash = hash_password(password, salt, iterations)
    return secrets.compare_digest(password_hash, compare_hash)



def alertERR(txt):
    return ft.AlertDialog(
        title="Notificacion",
        content=ft.Text(txt),
        alignment=ft.MainAxisAlignment.START

    )
class login(ft.ResponsiveRow):
    def __init__(self, page):
        
        super().__init__(expand=True)
        self.page = page
        # page.vertical_alignment=
        self.monitor = MonitorAlert(page=self.page)
        
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.alignment= ft.CrossAxisAlignment.CENTER
        # self.page=page
        self.correo = ft.Ref[ft.Row()]()
        self.pas = ft.Ref[ft.Row()]()
        print("lanzando login")
        self.controls = [
            ft.Container(
                        ft.Text("Inicio de sesión",
                                width=320,
                                size=30,
                                text_align="center",
                                weight="w900", 
                                color=ft.Colors.BLACK38),
                        padding=ft.padding.only(left=20, top=200, right=20, bottom=20),
                        # margin=ft.margin.only()

                    ),
                    ft.Container(
                        
                        content=ft.Row(
                           ref=self.correo ,
                            alignment=ft.MainAxisAlignment.CENTER ,
                            controls=[
                                ft.TextField(
                                
                                width=280,
                                height=40,
                                hint_text="Correo",
                                border="underline",
                                color="black",
                                prefix_icon=ft.Icons.EMAIL,
    
                                value="",
          
                            ),
                            ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.RED_200, visible=False),
                            ]

                        ),
                        padding=ft.padding.only(20,20),
                       
                    ),
                    ft.Container(
                        ft.Row(
                            ref=self.pas,
                            alignment=ft.MainAxisAlignment.CENTER ,
                            controls=[
                                ft.TextField(
                                
                                width=280,
                                height=40,
                                hint_text="Contraseña",
                                border="underline",
                                color="black",
                                # value="",
                                prefix_icon=ft.Icons.LOCK,
                                can_reveal_password=True,
                                password=True
                            ),
                               
                            ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.RED_200, visible=False),
                                
                            ]
                        ) ,
                        
                        padding=ft.padding.only(20,20),
                        

                    ),
                    ft.Container(
                        alignment=ft.alignment.center ,
                        content=ft.ElevatedButton(
                            
                            text="Entrar",
                            width=280,
                            on_click=self.entrar,
                            # disabled=True
                        ),
                        padding=ft.padding.only(20,20),
                        
                    
                    ),
                    ft.Text(
                        "Usuario o Contraseña invalida",
                        color="red",
                        visible=False,
                        width=280,
                        text_align=ft.alignment.center
                    )
        ]

    def entrar(self, e):
       
        
        email = None
        passsw = None
        # print(dir(self.correo))
        
        if self.correo.current.controls[0].value == "":
            
            
            self.correo.current.controls[1].visible = True
            self.correo.current.update()
            raise self.monitor.Alert(titulo="Advertencia", sms="Por favor ingresa el correo")
        elif "@" not in self.correo.current.controls[0].value:
           
            self.correo.current.controls[1].visible = True
            self.correo.current.update()
            raise self.monitor.Alert(titulo="Advertencia", sms="Por favor ingresa el correo adecuadamente")
        else:
            self.correo.current.controls[1].visible = False
            self.correo.current.controls[1].update()
            email = self.correo.current.controls[0].value
        
        if self.pas.current.controls[0].value == "":
   
            
            self.pas.current.controls[1].visible = True
            self.pas.current.update()
            raise self.monitor.Alert(titulo="Advertencia", sms="Por favor ingresa la contraseña")
        else:
            self.pas.current.controls[1].visible = False
            self.pas.current.controls[1].update()
            passsw = self.pas.current.controls[0].value
        
        if email != None and passsw != None:
            try:
                self.controls[3].content.disabled=True
                self.controls[3].update()
                passs = hashlib.sha256(passsw.encode('ascii'))
                
                
                data={   
                    "email":email,
                    "password":str(passs.hexdigest())

                }
                print(data)
                

                loginf = requests.post(os.environ.get("ulr_api")+"/user/login/",data=json.dumps(data),headers={"Content-Type":"application/json"})
                monitor = self.monitor.GetData(respuesta=loginf)
                self.controls[3].content.disabled=False
                self.controls[3].update()
             
                if monitor!=[]:
                    self.page.session.set("tokenkey", monitor[0]['token'])
                    self.page.clean()
                    self.page.add(base(self.page))
            except Exception as e:
                print(e)
                self.controls[3].content.disabled=False
                self.controls[3].update()
                self.monitor.AlertErrorServer(sms=str(e))
        pass
    # def build(self):
    #     vertical_alignment= ft.CrossAxisAlignment.CENTER

    #     print("aaaaaaaa")
        # return self.container_login
       

def main(page: ft.Page):

    load_dotenv()
    page.adaptive = True
   
    SECRET_KEY_TOKEN = os.environ.get("ulr_api")
    print(SECRET_KEY_TOKEN)
    page.padding = 0
    page.client_storage.set("prueba.cache", {})
    page.client_storage.set("prueba.cache.contactos", {})
    page.window.min_height = 820
    page.window.min_width = 530
    # horizontal_alignment
    page.vertical_alignment= ft.MainAxisAlignment.CENTER
    page.horizontal_alignment= ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    # page.add(login(page))
    if page.session.contains_key("tokenkey"):
        tokenkey = page.session.get("tokenkey")
        refresh = requests.post(os.environ.get("ulr_api")+"/user/logout/", headers={   
                "Authorization": "Bearer {0}".format(tokenkey)
            })
        if refresh.status_code == 200:
            page.add(base(page))
            # print( refresh.content['json'][0]['token'])
            page.session.set("tokenkey", refresh.content['json'][0]['token'])
        else:
            page.add(base(page)) 
        
    else:
        # page.session.set("tokenkey", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImZmYjI4NDUyLTExYmItNDM1NC1iM2U5LTRjMTlkOTkxOGI3NiIsInBrX3B1YmxpY2EiOiI2YTM1MjA1ZS00NDljLTRiODMtYjI1NS1lOWYxNDc1OTFjZTEifQ.WkIJTFeZ4fT8qrfypIfR4UNg2GB3npXCmERVWb8jiSk")
        # page.add(ui(page))
        # page.controls.append(login(page))
        page.add(login(page)) 
        # page.add(base(page))

ft.app(main)