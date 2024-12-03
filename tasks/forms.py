from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput
#
#
#
#class AgregarForm(forms.ModelForm):
#   
#    class Meta:
#        model = Book
#        fields= ["titulo", "autor", "ubicación", "pieza", "descripción", "día", "mes", "año", "Imagen"]
#
#
class CustomUserCreationForm(UserCreationForm): #creamos un form custom a partir del que django nos da Usercreationform
    email=forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username","email","password1", "password2"]
#
#class UpdateCuenta(forms.ModelForm):
#    password = forms.CharField(widget=PasswordInput(render_value=True),required=False)
#    class Meta:
#        model = User
#        fields = ["username", "first_name", "last_name", "email", "password"]
#    widgets = {
#            'password': forms.PasswordInput(render_value=True),
#        }
#    def clean_password(self):
#        password = self.cleaned_data.get('password')
#        if not password:
#            return self.instance.password  # Retorna la contraseña actual si no se proporciona una nueva
#        return password