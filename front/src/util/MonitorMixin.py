import os
import flet as ft
import requests



class ErrorMonitor(Exception):
    pass
class MonitorAlert():


    def __init__(self, page=None):
        self.page=page
    def handle_action_click(self, e):
        self.page.close(e.control.parent)
        pass
    def AlertErrorServer(self, titulo="Error", sms=""):
        # print(dir(self.page))
        self.page.open(ft.AlertDialog(
                        content=ft.Column(
                            adaptive=True,
                            controls=[
                                ft.Text(sms)
                        ] ),
                    title=ft.Text(titulo, text_align=ft.alignment.center),
                    adaptive=True,
                    alignment=ft.alignment.top_center,
                    actions=[
                        ft.TextButton("Ok", on_click=self.handle_action_click), 
                    ],
                ))
        
    def Alert(self, titulo="Error", sms=""): 
        
        self.page.open(ft.AlertDialog(
                        content=ft.Column(
                            adaptive=True,
                            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                            height=200,
                            controls=[
                                ft.Text(sms)
                        ] ),
                    title=ft.Text(titulo, text_align=ft.alignment.center),
                    adaptive=True,
                    alignment=ft.alignment.top_center,
                    actions=[
                        ft.TextButton("Ok", on_click=self.handle_action_click), 
                    ],
                ))
        # print(".............", sms)
        return ErrorMonitor("Gestor de errores de usuario.....")
    def GetData(self, respuesta:requests=None):
         
        jwt=False
        if self.page is None:
            return super(MonitorAlert, self).dispatch(respuesta,self.page )
        # print(respuesta)
        # print(respuesta.status_code)
        controles=[]
        respjson = respuesta.json()
        if respuesta.status_code == 200:
            
            if jwt:
                pass
            if respjson['status'] == 'success':
                titulo = "Operación exitosa"
            elif respjson['status'] == 'not_auth':
                titulo = "No Autorizado"
            elif respjson['status'] == 'error':
                titulo = "Error"
               
            for tex in respjson['menssage_user']:
                controles.append(ft.Text(tex['mensaje'] , expand=True))
            self.page.open(ft.AlertDialog(
                    content=ft.Column(
                        adaptive=True,
                        auto_scroll=True,
                        height=200,
                        
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        controls=controles ),
                    title= ft.Text(titulo, text_align=ft.alignment.center),
                    alignment=ft.alignment.top_center,
                    adaptive=True,
                    
                    actions=[
                        ft.TextButton("Ok", on_click=self.handle_action_click),
                        
                    ],

                ))
            return respjson['json']
        elif respuesta.status_code == 500:

        
            self.AlertErrorServer(sms="asdasdasda")
            ft.Page.open()
            self.page.open(control=ft.AlertDialog(
                        content=ft.Column(
                            adaptive=True,
                            # auto_scroll=True,
                            controls=[
                                ft.Text(str(respjson['menssage_server'][0]) )
                        ] ),
                        title=ft.Text("Error del servidor api"),
                        alignment=ft.alignment.top_center,
                        adaptive=True,
                        
                        actions=[
                            ft.TextButton("Ok", on_click=self.handle_action_click),
                            
                        ],
                    ))
            # self.page.open(control=ft.Text("aaaaaa"))
            print("555555555555555555555555")
            return respjson['json']
            # raise ErrorMonitor("Error en la repsuesta del api: "+ str(respjson['menssage_server']))
    