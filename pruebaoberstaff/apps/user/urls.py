from django.urls import path
from .views import  LoginUserAPI, LogoutUserApi
from .views import AdminUserApi, RolAPI, ContactoAPI



urlpatterns = [
	path('rol/', RolAPI.as_view(), name="RolAPI"),
	path('contacto', ContactoAPI.as_view(), name="ContactoAPI"),
	path('', AdminUserApi.as_view(), name="AdminUserApi"),
	path('login/', LoginUserAPI.as_view(), name="login"),
    path('logout/', LogoutUserApi.as_view(), name="logout"),
    # path('verificar/email', VerificarEmailAPI.as_view(), name="VerificarEmailAPI"),
  
]