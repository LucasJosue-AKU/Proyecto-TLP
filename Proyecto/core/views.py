from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Perfil
from api.models import Libro
from django.contrib.auth import authenticate, login, logout
from .recursos import obtener_portada, obtener_descripcion
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
        'libro_marcado' : False
    }

    if request.user.is_superuser is False and request.user.is_authenticated:
        contexto_libro['libro_marcado'] = request.user.perfil.favoritos.filter(id=id).exists()
    

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

    if request.method == "POST":

        nombre_usuario = request.POST['nombre']
        contraseña = request.POST['contraseña']

        usuario = authenticate(username=nombre_usuario, password=contraseña)

        if usuario is not None:        
            login(request, usuario)

            url = "Home"

            # si inicio sesion al intentar marcar un libro, se marca
            if request.GET.get('id'):

                id = int(request.GET.get('id'))

                if usuario.perfil.favoritos.filter(id=id).exists():
                    libro = Libro.objects.get(id=id)
                    usuario.perfil.favoritos.add(libro)

                url = request.GET.get('siguiente')

            return redirect(url)
        else:
            return render(request, 'core/inicio_sesion.html', {
                'error' : True,
            })
    else:
        return render(request, 'core/inicio_sesion.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('Home')

def marcar_libro(request, id):
    libro = Libro.objects.get(id=int(id))
    request.user.perfil.favoritos.add(libro)
    return redirect('Informacion', id)

def quitar_marcado(request, id):
    libro = Libro.objects.get(id=int(id))
    request.user.perfil.favoritos.remove(libro)

    if request.GET.get('siguiente'):
        siguiente = request.GET.get('siguiente')
        return redirect(siguiente)
    
    return redirect('Informacion', id)

def favoritos(request):

    contexto_libros = []

    libros = request.user.perfil.favoritos.all()

    for libro in libros:

        id = libro.id
        titulo = libro.Titulo
        autor = libro.Autor
        portada = obtener_portada(titulo)

        contexto_libros.append({
            'id' : id,
            'titulo' : titulo,
            'autor' : autor,
            'portada' : portada
        })
        
    return render(request, 'core/favoritos.html', {
        'libros' : contexto_libros,
    })