from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Perfil
from api.models import Libro
from django.contrib.auth import authenticate, login, logout
from .optimizaciones import obtener_portada, obtener_descripcion
import requests

def home(request):

    return render(request, 'core/home.html')

def catalogo(request):

    url_api = "http://127.0.0.1:8000/api/api/projects/"
    conexion_api = requests.get(url_api)
    datos_api = conexion_api.json()
    contexto_libros = []
    
    # Se obtienen las portadas de OpenLibrary
    for libro in datos_api:

        titulo = libro['Titulo']
        id = libro['id']
        portada = obtener_portada(titulo)

        contexto_libros.append({
            "id" : id,
            "portada" : portada
        })
        
    return render(request, 'core/catalogo.html', {
        'libros' : contexto_libros
    })

def informacion(request, id):

    url_api = "http://127.0.0.1:8000/api/api/projects/{}".format(id)
    conexion_api = requests.get(url_api)
    datos_api = conexion_api.json()
    
    titulo = datos_api['Titulo']
    id = datos_api['id']
    autor = datos_api['Autor']

    contexto_libro = {
        "id"    : id,
        "titulo" : titulo,
        "portada": obtener_portada(titulo),
        "descripcion" : obtener_descripcion(titulo),
        'autor' : autor,
    }

    return render(request, 'core/informacion.html', {
        'libro' : contexto_libro
    })


def registro(request):

    if request.method == "POST":

        estados_campos = {
            'nombre_usuario' : True,
            'correo_electronico' : True,
        }

        nombre_usuario = request.POST['nombre']
        correo_electronico = request.POST['correo']

        if User.objects.filter(username=nombre_usuario).exists():
            estados_campos['nombre_usuario'] = False

        if User.objects.filter(email=correo_electronico).exists():
            estados_campos['correo_electronico'] = False

        if estados_campos['nombre_usuario'] and estados_campos['correo_electronico']:

            contraseña = request.POST['contraseña']

            nuevo_usuario = User.objects.create_user(username=nombre_usuario, email=correo_electronico, password=contraseña)
            nuevo_usuario.save()

            # crear perfil
            perfil = Perfil.objects.create(usuario=nuevo_usuario)

            usuario = authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:

                login(request, usuario)
    
                if request.GET.get('id'):
                    id = int(request.GET.get('id'))
                    libro = Libro.objects.get(id=id)
                    perfil.favoritos.add(libro)

                url_anterior = request.GET.get('siguiente', 'Catalogo')
                return redirect(url_anterior)
        
        else: 
            return render(request, 'core/registro.html', {
                'estado_campos' : estados_campos,
            })
        
    return render(request, 'core/registro.html')
 

def inicio_sesion(request):
    return render(request, 'core/inicio_sesion.html')

    