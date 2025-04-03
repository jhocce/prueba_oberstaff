import flet as ft
from util.MonitorMixin import MonitorAlert
from util.request import request

class contactos(ft.ResponsiveRow, request):
    def __init__(self,page, contrl="list" ):
        
        super().__init__()

        expand=True
        self.page = page
        self.col=10
      
        self.controls=[]


    def GetDataComponet(self):
        da = {
            "Nombre":  "Contactos",
            "Icono": ft.Icon(ft.Icons.CONTACT_PHONE)
        }
        return da
    def getdata1(self):
        data = []
        dataRe = []
        resp = self.Get("/user/contacto")
        dataRe= resp.json()
       
        if resp.status_code == 500:
            return resp, None

        for dat in dataRe['json'][0]['data']:

            

            data.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(dat['Nombres'])),
                            ft.DataCell(ft.Text(dat['Apellidos'])),
                            ft.DataCell(ft.Text(dat['Telefono'])),
                            ft.DataCell(ft.Text(dat['Correo'])),
                           
                            ft.DataCell(ft.Row(controls=[
                                ft.IconButton( 
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.GREY,
                                    selected_icon_color=ft.Colors.PURPLE_200,
                                    icon_size=20,
                                    tooltip="Editar",
                                    data=[dat['pk_publica'],dataRe['entity']],
                                    on_click=self.actualizar
                                    ),
                                ft.IconButton( 
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.GREY,
                                    selected_icon_color=ft.Colors.PURPLE_200,
                                    icon_size=20,
                                    tooltip="Eliminar",
                                    data = (dat['pk_publica'],dataRe['entity']),
                                    on_click=self.eliminar
                                    ),
                                ft.IconButton( 
                                    icon=ft.Icons.VISIBILITY ,
                                    icon_color=ft.Colors.GREY,
                                    selected_icon_color=ft.Colors.PURPLE_200,
                                    icon_size=20,
                                    tooltip="Detallar",
                                    data = (dat['pk_publica'],dataRe['entity'])
                                    ),
                                ])),
                        ],
                    ))
        return resp, data


    def listar(self, e=None):
        print("listando")
        resp, data = self.getdata1()
        self.controls.clear()
        contenedor = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO,  
            expand=True,
        )
        contenedor.controls.append(
            ft.Container(
                expand=True,
                padding=ft.padding.only(right=100),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(right=30),
                            content=ft.Row(
                                controls=[
                                    ft.Text("Contactos", size=30),
                                    ft.Text("Listar")
                                        ]
                                    )
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.PERSON_ADD_ALT_1_OUTLINED,
                                    on_click=self.add_user
                                    
                                    )
                            ]
                        )  
            )
        )
        if data != None:
            contenedor.controls.append(
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Nombres")),
                        ft.DataColumn(ft.Text("Apellidos")),
                        ft.DataColumn(ft.Text("Telefono")),
                        ft.DataColumn(ft.Text("Correo")),
                        ft.DataColumn(ft.Text("Opciones")),
                       
                    ],
                    rows=data
            ),
            )
        else:
            contenedor.controls.append(
                ft.Text("No hay conexion"),
                
            )
            contenedor.controls.append(
              
                ft.Text(resp.json()['menssage_server'][0])
            )
           
           
        self.controls.append(contenedor)
        if e!=None:
            self.update()
    def actualizar_action(self, e):
        validado, data= self.validar(e)
        print(validado, data)
        if validado:
            resp = self.Update("/user/contacto", data=data, params={"pkquery":data['pk_publica']})
            dataRe= resp.json()
            print(dataRe)
            if resp.status_code != 200:
                self.page.open(ft.AlertDialog(
                                content=ft.Column(
                                    adaptive=True,
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                    height=200,
                                    controls=[
                                        ft.Text(dataRe['menssage_user'][0]['mensaje'])
                                ] ),
                            title=ft.Text("error", text_align=ft.alignment.center),
                            adaptive=True,
                            alignment=ft.alignment.top_center,
                            actions=[
                                ft.TextButton("Ok", on_click=self.handle_action_click), 
                            ],
                        ))
            if resp.status_code == 200:
                self.page.open(ft.AlertDialog(
                                content=ft.Column(
                                    adaptive=True,
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                    height=200,
                                    controls=[
                                        ft.Text(dataRe['menssage_user'][0]['mensaje'])
                                ] ),
                            title=ft.Text("Notificación", text_align=ft.alignment.center),
                            adaptive=True,
                            alignment=ft.alignment.top_center,
                            actions=[
                                ft.TextButton("Ok", on_click=self.handle_action_click), 
                            ],
                        ))
            print(resp)
            self.listar()
            self.update()
    def actualizar(self, e = None):
       nombres = ft.Ref[ft.TextField]()
       apellidos = ft.Ref[ft.TextField]()
       correo = ft.Ref[ft.TextField]()
       telefono = ft.Ref[ft.TextField]()
       key = "prueba.cache.{0}".format(e.control.data[1])
       pk_publica = e.control.data[0]
       cuerpo = self.page.client_storage.get(key)
       element = next((item for item in cuerpo['content']['data'] if item["pk_publica"] ==pk_publica), None)
       self.controls.clear()
       self.controls.append(
           ft.Container(
               padding=ft.padding.only(left=50),
               expand=True,
               content=ft.Column(
                   controls=[
                            ft.Container(
                                padding=ft.padding.only(right=100),
                                content=ft.Row(
                                    
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Text("Contactos", size=30),
                                                    ft.Text("Crear")
                                                        ]
                                                    )
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.LIST,
                                                    on_click=self.listar
                                                    
                                                    )
                                            ]
                                        )  
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Nombres",
                                            border="underline",
                                            color="black",
                                            ref=nombres,
                                            data="required",
                                            value=element['Nombres']
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Apellidos",
                                            border="underline",
                                            color="black",
                                            ref=apellidos,
                                            data="required",
                                            value=element['Apellidos']

                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                        
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="telefono",
                                            border="underline",
                                            color="black",
                                            ref=telefono,
                                            data="required",
                                            value=element['Telefono']

                                            
                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Correo",
                                            border="underline",
                                            color="black",
                                           ref=correo,
                                           data="required",
                                            value=element['Correo']
                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                        
                                ]
                            ),
                            
                            
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[ft.Container(
                                      
                                        content=ft.ElevatedButton(
                                            width=380,
                                            color="black",
                                            text="actualizar",
                                            on_click=self.actualizar_action,
                                            data=(pk_publica,[nombres, apellidos, telefono, correo,])
                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),]
                            )
                        ]
               )
           )
       )
    #    print(self)
       self.update()
       print("crear")
    def add_user(self, e=None):
       nombres = ft.Ref[ft.TextField]()
       apellidos = ft.Ref[ft.TextField]()
       correo = ft.Ref[ft.TextField]()
       telefono = ft.Ref[ft.TextField]()
      
       self.controls.clear()
       self.controls.append(
           ft.Container(
               padding=ft.padding.only(left=50),
               expand=True,
               content=ft.Column(
                   controls=[
                            ft.Container(
                                padding=ft.padding.only(right=100),
                                content=ft.Row(
                                    
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Text("Contactos", size=30),
                                                    ft.Text("Crear")
                                                        ]
                                                    )
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.LIST,
                                                    on_click=self.listar
                                                    
                                                    )
                                            ]
                                        )  
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Nombres",
                                            border="underline",
                                            color="black",
                                            ref=nombres,
                                            data="required"
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Apellidos",
                                            border="underline",
                                            color="black",
                                            ref=apellidos,
                                            data="required"
                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                        
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Telefono",
                                            border="underline",
                                            color="black",
                                            ref=telefono,
                                            data="required"
                                            
                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                    ft.Container(
                                        content=ft.TextField(
                                            width=380,
                                            label="Correo",
                                            border="underline",
                                            color="black",
                                           ref=correo,
                                           data="required"
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),
                                        
                                ]
                            ),
                            
                            
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[ft.Container(
                                      
                                        content=ft.ElevatedButton(
                                            width=380,
                                            color="black",
                                            text="Registrar",
                                            on_click=self.registrar,
                                            data=(None, [nombres, apellidos, telefono, correo,  ])
                                           
                                        ),
                                        padding=ft.padding.only(20,20)
                                    ),]
                            )
                        ]
               )
           )
       )
    #    print(self)
       self.update()
       print("crear")
    def eliminar_action(self, e=None):
      
            resp = self.Delete("/user/contacto", params={"pkquery":e.control.data})
            dataRe= resp.json()
         
            if resp.status_code != 200:
                self.page.open(ft.AlertDialog(
                                content=ft.Column(
                                    adaptive=True,
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                    height=200,
                                    controls=[
                                        ft.Text(dataRe['menssage_user'][0]['mensaje'])
                                ] ),
                            title=ft.Text("error", text_align=ft.alignment.center),
                            adaptive=True,
                            alignment=ft.alignment.top_center,
                            actions=[
                                ft.TextButton("Ok", on_click=self.handle_action_click), 
                            ],
                        ))
            if resp.status_code == 200:
                self.page.open(ft.AlertDialog(
                                content=ft.Column(
                                    adaptive=True,
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                                    height=200,
                                    controls=[
                                        ft.Text(dataRe['menssage_user'][0]['mensaje'])
                                ] ),
                            title=ft.Text("Notificación", text_align=ft.alignment.center),
                            adaptive=True,
                            alignment=ft.alignment.top_center,
                            actions=[
                                ft.TextButton("Ok", on_click=self.handle_action_click), 
                            ],
                        ))

            self.listar()
            self.update()
    def eliminar(self, e=None):
       
        def cerrar_modal(self,e=None):
            self.page.close(alert)
        alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Por favor confirma"),
            content=ft.Text("estas seguro de elimnar este {0}".format(e.control.data[1])),
            actions=[
                ft.TextButton("Yes", on_click=self.eliminar_action, data=e.control.data[0]),
                ft.TextButton("No", on_click=cerrar_modal),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
           
        )  
        self.page.open(alert)
        
    def validar(self, e):
        valid=True
        data={"pk_publica":e.control.data[0]}
        for input in e.control.data[1]:
            if input.current.data=="required" and input.current.value=="":
               
                input.current.prefix_icon=ft.Icons.WARNING_AMBER_OUTLINED
                input.current.bgcolor=ft.Colors.RED_100
                input.current.update()
                valid= False
            elif input.current.value != "":
                input.current.bgcolor=None
                input.current.prefix_icon=None
                input.current.update()
                data.update({
                    input.current.label:input.current.value
                })
            
               
        return (valid, data)
    
    def registrar(self, e):
        validado, data= self.validar(e)
        # print(validado, data)
        resp = self.Post("/user/contacto", data=data)
        dataRe= resp.json()

        if resp.status_code != 200:
           self.page.open(ft.AlertDialog(
                        content=ft.Column(
                            adaptive=True,
                            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                            height=200,
                            controls=[
                                ft.Text(dataRe['menssage_user'][0]['mensaje'])
                        ] ),
                    title=ft.Text("error", text_align=ft.alignment.center),
                    adaptive=True,
                    alignment=ft.alignment.top_center,
                    actions=[
                        ft.TextButton("Ok", on_click=self.handle_action_click), 
                    ],
                ))
        if resp.status_code == 200:
           self.page.open(ft.AlertDialog(
                        content=ft.Column(
                            adaptive=True,
                            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                            height=200,
                            controls=[
                                ft.Text(dataRe['menssage_user'][0]['mensaje'])
                        ] ),
                    title=ft.Text("Notificación", text_align=ft.alignment.center),
                    adaptive=True,
                    alignment=ft.alignment.top_center,
                    actions=[
                        ft.TextButton("Ok", on_click=self.handle_action_click), 
                    ],
                ))

        self.listar()
        self.update()
    def build(self):
       
        # self.monitor = MonitorAlert(page=self.page)
        self.listar()
        # print(self.controls)
        return self.controls