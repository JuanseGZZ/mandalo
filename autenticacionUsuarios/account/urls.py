from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('enviar-datos/', views.enviar_datos, name='enviar_datos'),
    path('unico/', views.subir_imagen, name='subir_imagen'),
    path('multiple/', views.multiple, name='mutiple'),
    path('eliminar-accountmultiple/',views. eliminar_todas_instancias_accountmultiple_y_archivos, name='eliminar_accountmultiple'),
    path('ruta/a/tu/funcion/', views.recibir_datos, name='recibir-datos'),
    path('stop-process/', views.stop_process, name='stop-process'),
    path('ruta-a-get-count/', views.get_count, name="get-count" ),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)