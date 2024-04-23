from django.db import models

# Create your models here.

#archivos
class Documento(models.Model):
    mensaje = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='imagenes/',null=True,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Accountmultiple(models.Model):
    mensajem = models.CharField(max_length=255)
    imagenm = models.ImageField(upload_to='imagenes/',null=True,blank=True)