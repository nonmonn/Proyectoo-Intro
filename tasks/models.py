from django.db import models
from django.contrib.auth.models import User

# models de books
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subgenre(models.Model):
    name = models.CharField(max_length=100)
    genero = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="subgeneros")

    def __str__(self):
        return f"{self.name} ({self.genero.name})"
    
# models.py
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")
    subgenre = models.ManyToManyField(Subgenre, related_name='books')
    description = models.TextField()
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_subgenres(self):
        return ", ".join([sub.name for sub in self.subgenre.all()])  # Crea una cadena con los nombres de los subgéneros

    get_subgenres.short_description = 'get_subgenres'  # Nombre de la columna en el admin

# models de quizapp 
class Quiz(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField()
    response_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Quiz for {self.book.title}"


# models de respuestas
class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer_text

# models de guardado de respuestas usuario
class UserQuizResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_responses")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="user_responses")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} answered {self.quiz.book.title} - {self.answer.answer_text}"
# models de recompensas 

class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField(default=1)

    def __str__(self):
        return self.name

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

