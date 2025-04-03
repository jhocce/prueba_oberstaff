import os
import requests
import flet as ft
from util.MonitorMixin import MonitorAlert
from componets.contactos import contactos

class base(ft.ResponsiveRow):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        self.alignment=ft.alignment.center
        self.bgcolor=ft.Colors.GREY_50 
        self.col=12

        self.componentes = [contactos(page=page) ]
        self.controls = [ 
            ft.Container(
                col=1,
                adaptive=True,
                border=ft.border.only(right=ft.border.BorderSide(1,  ft.Colors.BLUE_GREY_100)),
                content=ft.NavigationRail(
                    selected_index=0 ,
                    group_alignment=-0.8 ,
                    leading=ft.FloatingActionButton(icon=ft.Icons.HOME_OUTLINED),
                    expand=True ,
                    
                    indicator_color=ft.Colors.PURPLE_200,
                    destinations=[
                    ],
                    on_change=lambda e: self.getlienzo(e.control.selected_index),
                ) 
            ),
        
            ft.Column(
                col=10,
                controls=[
                  ft.Row(
                            adaptive=True,
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.Text("user"),
                                ft.IconButton(icon=ft.Icons.OUTBOND),
                             
                                
                            ]
                        ),
                ]
                  
            )
            
        ]
    
    def getlienzo(self, index):
        if len(self.controls[1].controls)==1:
            pass
        else:
            self.controls[1].controls.pop()
        self.controls[1].controls.append(self.componentes[index])
        self.controls[1].update()

    def build(self,):
        print("lanzando contructor")

        for contr in self.componentes:
            self.controls[0].content.destinations.append(
                 ft.NavigationBarDestination(
                            
                            icon=contr.GetDataComponet()['Icono'],
                            label=contr.GetDataComponet()['Nombre']
                        ),
            )
        pass