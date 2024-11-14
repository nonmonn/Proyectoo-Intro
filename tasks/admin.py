from django.contrib import admin
from .models import Book, Genre, Quiz, Subgenre, Answer, Reward, UserReward, UserQuizResponse

# Modelos de admin

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'get_subgenres']  # Usar el método aquí
    search_fields = ['title']

class Answerinline():
    model = Answer
    extra = 3

class Quizadmin(admin.ModelAdmin):
    inline =  [Answerinline]

class RewardAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'quiz']  # Campos que se mostrarán en la lista
    search_fields = ['name', 'quiz__book__title']  # Campos por los que se puede buscar
    list_filter = ['quiz']  # Filtros por los que se puede filtrar


# Register your models here.
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Quiz,Quizadmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Answer)
admin.site.register(Reward, RewardAdmin)
admin.site.register(UserReward)
admin.site.register(UserQuizResponse)