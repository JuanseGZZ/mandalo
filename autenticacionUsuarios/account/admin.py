from django.contrib import admin

# Register your models here.
from .models import Documento
from .models import Accountmultiple

# Registra tus modelos aquí
admin.site.register(Documento)
admin.site.register(Accountmultiple)