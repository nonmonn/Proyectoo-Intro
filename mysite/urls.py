"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name ='signup'),
    path('signin/', views.signin, name ='signin'),
    path('signout/', views.signout, name='signout'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.user_profile, name='user_profile'),
    path('books/', views.book_list, name='book_list'),
    path('buscar-libros/', views.search_books, name='search_books'),
    path('quiz/<int:book_id>/', views.quiz, name='quiz'),
    path('quiz_answer/<int:quiz_id>',views.quiz_detail, name='quiz_detail'),
    path('quiz_result/<int:quiz_id>', views.quiz_result, name='quiz_result'),
    path("signoff",views.prueba) #esto es una prueba de login signoff
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)