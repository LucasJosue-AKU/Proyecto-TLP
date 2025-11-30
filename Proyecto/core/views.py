from django.shortcuts import render, HttpResponse
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
        titulo = libro["Titulo"]
        id = libro["id"]
        print(id)
        url_openLibrary = "https://openlibrary.org/search.json?title={}".format(titulo)
        conexion_openLibrary = requests.get(url_openLibrary)
        datos_openLibrary = conexion_openLibrary.json()
        portada = ""

        for doc in datos_openLibrary["docs"]:
            if "cover_edition_key" in doc:
                portada = "https://covers.openlibrary.org/b/olid/{}-L.jpg".format(
                    doc["cover_edition_key"]
                )
                break

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
    
    titulo = datos_api["Titulo"]
    url_google_api = "https://www.googleapis.com/books/v1/volumes?q=intitle:{}".format(titulo)
    conexion_google_api = requests.get(url_google_api)
    datos_libro = conexion_google_api.json()
    descripcion = ""

    for item in datos_libro["items"][:10]:
        if "volumeInfo" in item and "description" in item["volumeInfo"]:
            descripcion = item["volumeInfo"]["description"]
            break

    contexto_libro = {
        "titulo" : titulo,
        "descripcion" : descripcion,
    }

    return render(request, 'core/informacion.html', {
        'libro' : contexto_libro
    })
