from django.contrib import admin
from .models import Book
from .models import Genre
from .models import Quiz
from .models import Reward
from .models import Achievement
from .models import Recommendation
# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Quiz)
admin.site.register(Reward)
admin.site.register(Achievement)
admin.site.register(Recommendation)
