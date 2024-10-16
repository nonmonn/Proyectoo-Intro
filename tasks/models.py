from django.db import models

# Create your models here.

# models de books
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")
    description = models.TextField()
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)  # Para la portada del libro

    def __str__(self):
        return self.title


# models de quizapp 
class Quiz(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    other_options = models.CharField(max_length=500)  # Opciones incorrectas separadas por comas

    def __str__(self):
        return f"Quiz for {self.book.title}"

# models de recompensas 
class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    level_required = models.IntegerField(default=1)

    def __str__(self):
        return self.name

# modelos para logro de usuarios. Aquí puedes relacionar a los usuarios con los logros obtenidos:

from django.contrib.auth.models import User

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} earned {self.reward.name}"

# models para sistema de recomendaciones 
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_recommended = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.book.title}"

