from django.contrib import admin
from .models import Book, Genre, Quiz, Reward, Achievement, Recommendation, Subgenre

# Modelos de admin

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'get_subgenres']  # Usar el método aquí
    search_fields = ['title']

# Register your models here.
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Quiz)
admin.site.register(Reward)
admin.site.register(Achievement)
admin.site.register(Recommendation)
admin.site.register(Book, BookAdmin)
