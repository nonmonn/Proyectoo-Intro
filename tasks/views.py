from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.http import HttpResponse  

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
    }) #de esta vola se pone el .html del signup
    else:
        if request.POST['password1'] == request.POST['password2']: #comparamos las contraseñas
            try: #si no existe el usuario pasa esto
                #Registra usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) #como son iguales da igual si es password 1 o 2
                user.save()
                return HttpResponse('User created successfully') # "Se creo de manera correcta el usuario"
            except: #si se intenta registar usuario que ya existe
                return render(request, 'signup.html',{
        'form': UserCreationForm,
        'error': 'Username already exists'
    })
        #para cuando se equivoquen escribiendo las contraseñas
        return render(request, 'signup.html',{
        'form': UserCreationForm,
        'error': 'Password do not match'
    })

def home(request):
    return render(request, 'home.html') #pone el .html del home

def prueba(request):
    return render(request, "index.html") #esto es una prueba de login signoff