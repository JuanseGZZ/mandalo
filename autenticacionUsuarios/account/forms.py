from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from .models import *

class MiModeloForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['mensaje','numero','nombre','imagen']
        widgets = {
            'mensaje': forms.TextInput(attrs={
                'placeholder': 'Mensaje',
                'class': 'input-field'
            }),
            'numero': forms.TextInput(attrs={
                'placeholder': 'Ingresa un número',
                'class': 'input-field',
            }),
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Nombre completo',
                'class': 'input-field'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'accept': 'image/png,video/mp4',  # Limita a archivos de imagen
                'class': 'file-input'
            }),
        }


class Formmultiple(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Formmultiple, self).__init__(*args, **kwargs)
        
        # Modificar el contenido del label para el campo 'mensajem'
        self.fields['mensajem'].label = ""

        self.fields['imagenm'].label = "Agregue su imagen(PNG) o video(MP4)"

    
    class Meta:
        model = Accountmultiple
        fields = ['mensajem', 'imagenm']
        widgets = {
            'mensajem': forms.TextInput(attrs={'placeholder': 'Mensaje', 'class': 'file-input mensaje'}),
            'imagenm': forms.ClearableFileInput(attrs={'accept': 'image/png,video/mp4','class': 'file-input imagen'}),
        }

