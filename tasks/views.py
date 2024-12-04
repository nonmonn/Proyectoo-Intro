from django.conf import settings
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from .models import Book, Genre, Subgenre, Quiz, UserQuizResponse, Answer, Reward, UserReward
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CustomUserCreationForm



def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm()
        })

    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            dominio_mail = email.split('@')[-1]

            try:
                # Crear usuario
                user = User.objects.create_user(username=username, email=email, password=password)

                # Verificar dominio del correo
                if dominio_mail == 'usm.cl':
                    user.is_staff = True
                    user.is_superuser = True
                else:
                    # Asignar al grupo 'Usuario'
                    group, created = Group.objects.get_or_create(name='Usuario')  # Crea el grupo si no existe
                    user.groups.add(group)

                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Este nombre de usuario o correo ya existe'
                })

        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Por favor, corrige los errores en el formulario'
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

@login_required
def user_profile(request):
    user = request.user
    user_quizzes = UserQuizResponse.objects.filter(user=user).select_related('quiz', 'quiz__book', 'answer')
    user_rewards = UserReward.objects.filter(user=user).select_related('reward')

    context = {
        'user': user,
        'user_quizzes': user_quizzes,
        'user_rewards': user_rewards,
    }
    return render(request, 'profile.html', context)

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
    quizzes = Quiz.objects.filter(book=book)

    # Filtrar las preguntas que el usuario ya ha respondido correctamente
    answered_correctly = UserQuizResponse.objects.filter(
        user=request.user,
        is_correct=True
    ).values_list('quiz_id', flat=True)

    # Obtener solo las preguntas que el usuario no ha respondido o ha respondido incorrectamente
    quizzes_to_answer = quizzes.exclude(id__in=answered_correctly)

    # Mostrar un mensaje si no hay más preguntas para responder
    if not quizzes_to_answer.exists():
        return render(request, 'allquizes.html', {
            'book': book,  # Asegúrate de incluir la información del libro
            'quizzes': None  # O explícitamente pasa un valor que indique que no hay cuestionarios
        })

    return render(request, 'allquizes.html', {
        'book': book,
        'quizzes': quizzes_to_answer
    })

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = quiz.answers.all()

    if request.method == "POST":
        selected_answer_id = request.POST.get('answer')
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)

        # Verificar si la respuesta es correcta
        is_correct = selected_answer.is_correct

        if is_correct:
            # Guardar la respuesta correcta del usuario
            UserQuizResponse.objects.create(
                user=request.user,
                quiz=quiz,
                answer=selected_answer,
                is_correct=is_correct
            )

            # Incrementar el contador de respuestas
            quiz.response_count += 1
            quiz.save()

            # Asignar la recompensa al usuario si aún no la tiene
            reward = Reward.objects.filter(quiz=quiz).first()
            if reward:
                user_reward_exists = UserReward.objects.filter(user=request.user, reward=reward).exists()
                if not user_reward_exists:
                    UserReward.objects.create(user=request.user, reward=reward)

            # Redirigir a la página de resultados
            return redirect('quiz_result', quiz_id=quiz.id)
        else:
            # Guardar la respuesta incorrecta del usuario
            UserQuizResponse.objects.create(
                user=request.user,
                quiz=quiz,
                answer=selected_answer,
                is_correct=is_correct
            )
            quiz.save()
            # Redirigir a la página de resultados
            return redirect('quiz_result', quiz_id=quiz.id)
        

    return render(request, 'quiz_detail.html', {'quiz': quiz, 'answers': answers})

@login_required
def book_list(request):
    genre_id = request.GET.get('genre')
    
    # Annotate each book with the total count of responses from all related quizzes
    books = (
        Book.objects.annotate(total_responses=Count('quizzes__user_responses'))
        .order_by('-total_responses')
    )
    
    if genre_id:
        books = books.filter(genre_id=genre_id)
    
    genres = Genre.objects.all()
    return render(request, 'books.html', {'books': books, 'genres': genres})

@login_required
def quiz_result(request, quiz_id):
    responses = UserQuizResponse.objects.filter(quiz_id=quiz_id, user=request.user)
    return render(request, 'quiz_result.html', {'responses': responses})
#
#
#@permission_required('myapp.view_agregar')
#@login_required(login_url="/accounts/login/")
#def Book(request):
#    data = {'form': AgregarForm()}
#    if request.method == 'POST':
#        formulario = AgregarForm(request.POST, request.FILES)
#        if formulario.is_valid():
#            agregar= formulario.save(commit=False)
#            nueva_pieza = formulario.save()
#            url_pieza = f"https://AdminQR.pythonanywhere.com/pieza/{nueva_pieza.id}/"
#            qr_img = qrcode.make(url_pieza)
#            qr_filename = f'qr_{nueva_pieza.id}.png'
#            qr_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', qr_filename)
#            qr_img.save(qr_path)
#            nueva_pieza.codigo_qr = f"qr_codes/{qr_filename}"
#            nueva_pieza.save()
#            data["mensaje"] = "Guardado y QR generado"
#            data["qr_url"] = os.path.join(settings.MEDIA_URL, 'qr_codes', qr_filename)
#            # Combina los valores de año, mes y día según los datos disponibles
#            year = formulario.cleaned_data.get("año")
#            month = formulario.cleaned_data.get("mes")
#            day = formulario.cleaned_data.get("día")
#
#            if year and month and day:
#                agregar.fecha = date(year, month, day)
#            elif year and month:
#                agregar.fecha = date(year, month, 1)
#            elif year:
#                agregar.fecha = date(year, 1, 1)
#            agregar.save()
#        else:
#            data["form"] = formulario
#    return render(request, 'myapp/Pieza/agregar.html', data)
#