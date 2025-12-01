from django.core.cache import cache
import requests
        
def obtener_portada(titulo):

    # Agregar al cache y si ya esta, se devuelve de ahi
    llave = "portada_{}".format(titulo)
    portada = cache.get(llave)
    if portada:
        return portada
    
    url_openLibrary = "https://openlibrary.org/search.json?title={}".format(titulo)
    conexion_openLibrary = requests.get(url_openLibrary)
    datos_openLibrary = conexion_openLibrary.json()
    portada = ""
    
    # Si existen muchos doc en docs, se itera 10 o hasta encontrar el primero que tenga portada

    for doc in datos_openLibrary["docs"][:10]:
        if "cover_edition_key" in doc:
            portada = "https://covers.openlibrary.org/b/olid/{}-L.jpg".format(
                doc["cover_edition_key"]
            )
            break
    
    cache.set(llave, portada, timeout=60*60)
    return portada

def obtener_datos_google_books(titulo):

    datos = {
        'descripcion' : "",
        'puntuacion' : "",
    }

    llave_descripcion = "descripcion_{}".format(titulo)
    llave_puntuacion = "puntuacion_{}".format(titulo)

    datos['descripcion'] = cache.get(llave_descripcion)
    datos['puntuacion'] = cache.get(llave_puntuacion)
    
    if datos['descripcion'] and datos['puntuacion']:
        return datos
    
    url_google_api = "https://www.googleapis.com/books/v1/volumes?q=intitle:{}".format(titulo)
    conexion_google_api = requests.get(url_google_api)
    datos_libro = conexion_google_api.json()
    datos['descripcion'] = ""
    datos["puntuacion"] = ""

    for item in datos_libro["items"][:10]:
        if "volumeInfo" in item:
            if datos["descripcion"] == "":
                datos["descripcion"] = item["volumeInfo"]["description"]
            elif datos["puntuacion"] == "":
                datos["puntuacion"] = item["volumeInfo"]["averageRating"]
            else:
                break
            
    cache.set(llave_descripcion, datos["descripcion"], 60*60)
    cache.set(llave_puntuacion, datos["puntuacion"], 60*60)
    return datos