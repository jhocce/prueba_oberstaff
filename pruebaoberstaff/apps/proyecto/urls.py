from django.urls import path
from .views import  ProyectoAPI, emailreportesAPI, TareaAPI, comentarioAPI


urlpatterns = [
	path('', ProyectoAPI.as_view(), name="ProyectoAPI"),
	path('emailreportes', emailreportesAPI.as_view(), name="emailreportes"),
	path('tarea', TareaAPI.as_view(), name="TareaAPI"),
	path('comentario', comentarioAPI.as_view(), name="comentarioAPI"),

    # path('verificar/email', VerificarEmailAPI.as_view(), name="VerificarEmailAPI"),
  
]