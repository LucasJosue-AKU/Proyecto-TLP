from django.shortcuts import render, HttpResponse
import requests

def home(request):

    url_api = "http://127.0.0.1:8000/api/api/projects/"
    conexion_api = requests.get(url_api)
    datos_api = conexion_api.json()

    return render(request, 'core/home.html', {})