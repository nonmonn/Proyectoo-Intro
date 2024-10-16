from django.db import models

# Create your models here.
class Quiz(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    other_options = models.CharField(max_length=500)  # Opciones incorrectas separadas por comas

    def __str__(self):
        return f"Quiz for {self.book.title}"