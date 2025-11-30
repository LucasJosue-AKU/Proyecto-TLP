from django.shortcuts import render, HttpResponse
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
    autor = datos_api['Autor']

    contexto_libro = {
        "titulo" : titulo,
        "portada": obtener_portada(titulo),
        "descripcion" : obtener_descripcion(titulo),
        'autor' : autor,
    }

    return render(request, 'core/informacion.html', {
        'libro' : contexto_libro
    })


def registro(request):
    return render(request, 'core/registro.html')