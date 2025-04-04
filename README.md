# Proyecto Oberstaff

Este repositorio contiene dos proyectos principales:

1. **Backend**: Un proyecto desarrollado en Django Rest Framework llamado `pruebaoberstaff`.
2. **Frontend**: Una aplicación desarrollada en Flet.

Ambos proyectos están configurados para ejecutarse en contenedores Docker.

---

## Estructura del Proyecto
├── front/ # Código fuente del frontend 
│   ├── src/ # Código principal de la aplicación Flet 
│   ├── Dockerfile # Configuración de Docker para el frontend 
│   └── requirements.txt # Dependencias del frontend 
├── pruebaoberstaff/ # Código fuente del backend 
│   ├── apps/ # Aplicaciones del proyecto Django 
│   ├── Dockerfile # Configuración de Docker para el backend 
│   ├── manage.py # Script de gestión de Django
│   ├── entry.sh # se ejecuta una vez construida la imagen en el contenedor.
│   ├── GenKeRsa.py # Script que generar las claves RSA en .pem
│   └── requirements.txt # Dependencias del backend 
└── docker-compose.yml # Configuración para ejecutar ambos servicios


---

## Requisitos Previos

- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados en tu máquina.

---

## Configuración Inicial

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio

## Configuración de Variables de Entorno

2. Crea los archivos `.env` necesarios para ambos proyectos (en teoría los .env no debería estar en el repositorio pero solo para fines de prueba se dejara tal cual en el sistema de archivos) :  
   ○ **Frontend**: `front/.env`  
   ○ **Backend**: `pruebaoberstaff/.env`  


## Ejecución con Docker
1. Construye y levanta los contenedores:
    ``` docker-compose up --build ```

## Accede a las aplicaciones:

1. Frontend: http://localhost:9000 (puerto configurado en el Dockerfile del frontend).
2. Backend: http://localhost:8000 (puerto configurado en el Dockerfile del backend).

## Documentación en backend

    http://localhost:8000/swagger/
    
    http://localhost:8000/redoc/

## Data de prueba
El siguiente es un usuario de prueba del tipo administrador.

* usuario: prueba@prueba.com
* contraseña: 123456