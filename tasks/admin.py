from django.contrib import admin
from .models import Book, Genre, Quiz, Reward, Achievement, Recommendation, Subgenre, Answer

# Modelos de admin

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'get_subgenres']  # Usar el método aquí
    search_fields = ['title']

class Answerinline():
    model = Answer
    extra = 3

class Quizadmin(admin.ModelAdmin):
    inline =  [Answerinline]

# Register your models here.
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Quiz,Quizadmin)
admin.site.register(Reward)
admin.site.register(Achievement)
admin.site.register(Recommendation)
admin.site.register(Book, BookAdmin)
admin.site.register(Answer)
