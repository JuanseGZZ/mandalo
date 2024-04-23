from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .forms import LoginForm

import requests
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password']) # None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('El usuario no esta activo')
            else:
                return HttpResponse('La información no es correcta')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    
@login_required
def dashboard(request):
    form = MiModeloForm()
    return render(request,'account/dashboard.html',{'form': form})

@login_required
@csrf_exempt  # Deshabilita la verificación de CSRF temporalmente para simplificar
def enviar_datos(request):
    if request.method == 'POST':
        # Obtén los datos enviados desde el HTML
        data = request.json
        numero = data['numero']
        mensaje = data['mensaje']

        # Prepara los datos para enviar a Node.js
        datos_a_node = {
            "numero": numero,
            "mensaje": mensaje,
        }

        # URL del endpoint de tu servidor Node.js
        url_node = 'http://127.0.0.1:3002/enviar-mensaje'

        # Envía los datos a Node.js
        response = requests.post(url_node, json=datos_a_node)
        if response.status_code == 200:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseRedirect(reverse('dashboard'))

from .forms import MiModeloForm
from django.core.files.storage import default_storage
from requests.exceptions import RequestException
@login_required
def subir_imagen(request):
    if request.method == 'POST':
        form = MiModeloForm(request.POST, request.FILES)
        if form.is_valid():
            instancia = form.save()
            url = 'http://127.0.0.1:3002/enviar-mensaje'
            data = {
                "phone": instancia.numero,
                "mensaje": "hola " + instancia.nombre+ " " + instancia.mensaje,
            }

            # Añade la URL de la imagen si existe y es accesible.
            if instancia.imagen and hasattr(instancia.imagen, 'url'):
                try:
                    instancia.imagen.file
                    data["media"] = instancia.imagen.url
                except Exception as e:
                    print(f"No se pudo acceder al archivo de imagen: {e}")

            headers = {'Content-Type': 'application/json'}

            # Intenta enviar los datos. Captura cualquier excepción relacionada con la solicitud.
            try:
                response = requests.post(url, json=data, headers=headers)
                # Aquí puedes verificar el estado de la respuesta y actuar en consecuencia.
                if response.status_code == 200:
                    print("Mensaje enviado con éxito.")
                else:
                    print(f"Error al enviar el mensaje. Código de estado: {response.status_code}")
            except RequestException as e:
                print(f"Error al realizar la solicitud: {e}")

            # Elimina la instancia y el archivo asociado.
            if instancia.imagen:
                try:
        # En lugar de instancia.imagen.file, que abre el archivo,
        # utiliza atributos que no requieren abrirlo, como instancia.imagen.name o instancia.imagen.url.
        
        # Si necesitas asegurarte de que el archivo existe sin abrirlo:
                    if default_storage.exists(instancia.imagen.name):
                        default_storage.delete(instancia.imagen.name)
                        print("Archivo de imagen eliminado con éxito.")
                except Exception as e:
                    print(f"Error al eliminar el archivo de imagen: {e}")
            instancia.delete()
            
            return render(request, 'account/unico.html', {'form': form})
    else:
        form = MiModeloForm()
    return render(request, 'account/unico.html', {'form': form})

from .forms import Formmultiple

@login_required
def multiple(request):
    estado = False  # Inicializa la variable estado como False
    if request.method == 'POST':
        form = Formmultiple(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.cleaned_data.get('imagenm', None)  # Asumiendo que 'imagen' es el nombre del campo en tu formulario
            if imagen:
                instancia = form.save()
                estado = True  # Cambia el estado a True si la imagen se carga correctamente
            else:
                estado = True
            # Independientemente de si se cargó una imagen, devuelve el formulario y el estado
            return render(request, 'account/multiple.html', {'form': form, 'estado': estado})
        else:
            # Si el formulario no es válido, también retorna el formulario con el estado (que seguirá siendo False)
            return render(request, 'account/multiple.html', {'form': form, 'estado': estado})
    else:
        form = Formmultiple()
    # Si no es un POST, muestra el formulario vacío y el estado sigue siendo False
    return render(request, 'account/multiple.html', {'form': form, 'estado': estado})

import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Accountmultiple

@login_required
def eliminar_todas_instancias_accountmultiple_y_archivos(request):
    # Opcional: Verifica aquí si el usuario tiene los permisos adecuados
    
    instancias = Accountmultiple.objects.all()
    for instancia in instancias:
        if instancia.imagenm:  # Asegurándose de que la instancia tenga un archivo asociado
            try:
                # Construye el path completo del archivo
                path = os.path.join(settings.MEDIA_ROOT, instancia.imagenm.name)
                os.remove(path)  # Elimina el archivo del sistema de archivos
            except Exception as e:
                print(f"Error al eliminar el archivo {instancia.imagenm.name}: {e}")
    
    # Una vez eliminados los archivos, elimina todas las instancias del modelo
    instancias.delete()
    
    # Redirecciona a alguna página, por ejemplo, a la del dashboard
    return HttpResponseRedirect(reverse('account/multiple.html'))



# forit


import threading
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from time import sleep

# Variable global para controlar la ejecución del hilo
stop_requested = False
in_proces = False
howless = 0
lock = threading.Lock()  # Bloqueo para manejar acceso seguro a 'howless'

def send_messages(data):#falta agregar el cada 30 pausar 15
    global stop_requested, in_proces, howless
    in_proces = True
    url = 'http://127.0.0.1:3002/enviar-mensaje'
    headers = {'Content-Type': 'application/json'}

    for contacto in data['contactos']:
        if howless >0 and howless % 30 == 0:
            sleep(900)
        elif howless >0 and howless % 200 == 0:
            sleep(21600)
        if stop_requested:
            print("Envío detenido por el usuario.")
            in_proces = False
            break

        # Construye el mensaje, incluyendo el nombre del contacto
        mensaje = f"Hola {contacto['nombre']}, {data['mensaje']}"
        payload = {
            "phone": contacto['numero'],
            "mensaje": mensaje,
        }
        sleep(5)
        # Si 'link' está presente y no es null, inclúyelo en el payload
        if data.get('link'):
            payload['media'] = data['link']

        #print(mensaje)
        #Intenta enviar el mensaje usando la API externa
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print("Mensaje enviado con éxito.")
            else:
                print(f"Error al enviar el mensaje. Código de estado: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
        print(mensaje,payload)
        with lock:
            howless += 1  # Acceso seguro al incrementar
    in_proces = False
    howless = 0

@csrf_exempt
@login_required
def recibir_datos(request):
    if request.method == 'POST':
        global stop_requested
        stop_requested = False  # Reiniciar la solicitud de detener antes de cada nueva ejecución
        #print(request.body)  # Debug para ver el cuerpo de la solicitud
        data = json.loads(request.body)
        #print(data)  # Debug para ver el contenido parseado
        if in_proces == False:
            threading.Thread(target=send_messages, args=(data,)).start()
        return JsonResponse({'status': 'success', 'message': 'Proceso iniciado'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



@csrf_exempt
@login_required
def stop_process(request):
    global stop_requested
    if request.method == 'POST':
        stop_requested = True
        howless = 0
        return JsonResponse({'status': 'success', 'message': 'Proceso detenido'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def get_count(request):
    global howless
    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'message': 'Conteo de mensajes', 'count': howless})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

