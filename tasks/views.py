from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from .models import Book, Genre, Subgenre, Quiz, UserQuizResponse, Answer
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    }) #de esta vola se pone el .html del signup

    else:
        if request.POST['password1'] == request.POST['password2']: #comparamos las contraseñas
            try: #si no existe el usuario pasa esto
                #Registra usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1']) #como son iguales da igual si es password 1 o 2
                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError: #si se intenta registar usuario que ya existe
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Este nombre de usuario ya existe'
                })

        #para cuando se equivoquen escribiendo las contraseñas
        return render(request, 'signup.html',{
        'form': UserCreationForm,
        'error': 'Las contraseñas no coinciden'
    })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm    
        })

    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,  
                'error' : 'El nombre de usuario o la contraseña son incorrectos'  
            })

        else:
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html') #pone el .html del home

def prueba(request):
    return render(request, "index.html") #esto es una prueba de login signoff

@login_required
def book_list(request):
    genre_id = request.GET.get('genre')
    if genre_id:
        books = Book.objects.filter(genre_id=genre_id)
    else:
        books = Book.objects.all()
    
    genres = Genre.objects.all()
    return render(request, 'books.html', {'books': books, 'genres': genres})

@login_required
def search_books(request):
    # Obtener todos los géneros y subgéneros
    genres = Genre.objects.all()
    subgenres = Subgenre.objects.all()
    
    # Obtener parámetros de búsqueda
    selected_genre_id = request.GET.get('genre')
    selected_subgenre_id = request.GET.get('subgenre')

    # Filtrar libros según el género y subgénero seleccionados
    books = Book.objects.all()
    
    if selected_genre_id:
        books = books.filter(genre__id=selected_genre_id)
    
    if selected_subgenre_id:
        books = books.filter(subgenre__id=selected_subgenre_id)

    context = {
        'books': books,
        'genres': genres,
        'subgenres': subgenres,
        'selected_genre_id': selected_genre_id,
        'selected_subgenre_id': selected_subgenre_id,
    }
    
    return render(request, 'search_books.html', context)

@login_required
def quiz(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    quizzes = Quiz.objects.filter(book=book)  # Obtener todas las preguntas relacionadas con el libro

    if request.method == 'POST':
        # Aquí puedes manejar la lógica de las respuestas del cuestionario
        # Por ejemplo, podrías verificar las respuestas y dar feedback
        pass  # Lógica para manejar respuestas aquí

    return render(request, 'allquizes.html', {'book': book, 'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = quiz.answers.all()

    if request.method == "POST":
        selected_answer_id = request.POST.get('answer')
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)

        # Verificar si la respuesta es correcta
        is_correct = selected_answer.is_correct

        # Crear la respuesta del usuario
        UserQuizResponse.objects.create(
            user=request.user,
            quiz=quiz,
            answer=selected_answer,
            is_correct=is_correct
        )

        # Incrementar el contador de respuestas
        quiz.response_count += 1
        quiz.save()

        return redirect('quiz_result', quiz_id=quiz.id)  # Redirigir a una página de resultados

    return render(request, 'quiz_detail.html', {'quiz': quiz, 'answers': answers})

@login_required
def quiz_result(request, quiz_id):
    responses = UserQuizResponse.objects.filter(quiz_id=quiz_id, user=request.user)
    return render(request, 'quiz_result.html', {'responses': responses})