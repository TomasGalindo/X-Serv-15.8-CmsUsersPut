from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
# Create your views here.
from cms_put.models import Page


def writeBase(request):
    respuesta = "Listado de las paginas que tienes guardadas. "
    lista_paginas = Page.objects.all()
    for pagina in lista_paginas:
        respuesta += "<br>" + pagina.name + " Id = " + str(pagina.id)

    if request.user.is_authenticated():
        respuesta += ("<br><br>Logged in as " + request.user.username +
                      "<a href='/logout'> Logout </a>")
    else:
        respuesta += ("<br><br>Not Logged in. <a href='/login/'> Login </a>")
    return HttpResponse(respuesta)


# BUSCANDO A TRAVES DEL IDENTIFICADOR
@csrf_exempt
def pagina(request, nameRecurso):
    if request.method == "GET":
        # Buscar en la base de datos
        try:
            pagina = Page.objects.get(name=nameRecurso)
            # si existe
            respuesta = "Pagina que has pedido: " + pagina.page
        except Page.DoesNotExist:
            # no existe
            respuesta = "No existe la pagina " + nameRecurso
            respuesta += "<form action='/" + nameRecurso + "' method='post'>"
            respuesta += "Name: <input type= 'text' name='name'>"
            respuesta += "Page: <input type= 'text' name='page'>"
            respuesta += "<input type= 'submit' value='enviar'>"
            respuesta += "</form>"

        if request.user.is_authenticated():
            respuesta += ("<br>Logged in as " + request.user.username +
                          "<a href='/logout'> Logout </a>")
        else:
            respuesta += ("<br>Not Logged in. <a href='/login/'> Login </a>")

    elif request.method == "POST":
        print("DETECTO POST")
        if request.user.is_authenticated():
            name = request.POST['name']
            page = request.POST['page']
            # Pngo el try, por si acaso me cambian el nombre
            try:
                Pagina = Page.objects.get(name=name)
                respuesta = ("No se puede añadir porque ya existe")
            except Page.DoesNotExist:
                pagina = Page(name=name, page=page)
                pagina.save()
                respuesta = "HE HECHO UN POST, lo he guardado"
            respuesta += ("<br>Logged in as " + request.user.username +
                          "<a href='/logout'> Logout </a>")
        else:
            respuesta = ("Necesitas logearte para introducir en " +
                         "la base de datos" + "<a href='/login/'> Login</a>")
    elif request.method == "PUT":
        print("DETECTO PUT")
        if request.user.is_authenticated():
            # busco por el nombre
            # obligo a que no se puedan repetir los recursos
            try:
                Pagina = Page.objects.get(name=nameRecurso)
                # Ya existe la pagina
                respuesta = ("No se puede añadir porque ya existe")
            except Page.DoesNotExist:
                campoPagina = request.body.decode('utf-8')
                pagina = Page(name=nameRecurso, page=campoPagina)
                pagina.save()
                respuesta = "He detectado un PUT, Guardado"
            respuesta += ("<br>Logged in as " + request.user.username +
                          "<a href='/logout'> Logout </a>")
        else:
            respuesta = ("Necesitas logearte para introducir en " +
                         "la base de datos" + "<a href='/login/'> Login</a>")
    else:
        respuesta = "NO PUEDES HACER ESTA OPERACION"
        if request.user.is_authenticated():
            respuesta += ("<br>Logged in as " + request.user.username +
                          "<a href='/logout'> Logout </a>")
        else:
            respuesta += ("<br>Not Logged in. <a href='/login/'> Login </a>")
    return HttpResponse(respuesta)
