from django.contrib import admin
from .models import Book
from .models import Genre
from .models import Quiz
from .models import Reward
from .models import Achievement
from .models import Recommendation

# Modelos de admin

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre']
    search_fields = ['title']

# Register your models here.
admin.site.register(Genre)
admin.site.register(Quiz)
admin.site.register(Reward)
admin.site.register(Achievement)
admin.site.register(Recommendation)
admin.site.register(Book, BookAdmin)
