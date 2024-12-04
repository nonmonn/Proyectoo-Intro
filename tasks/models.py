from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
#from django.utils import timezone
#from datetime import date

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
    image = models.ImageField(upload_to='rewards/', null=True, blank=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='rewards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_edit_rewards", "Can edit rewards"),
        ]

    def __str__(self):
        return self.name

class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='user_rewards')
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"
@receiver(post_delete, sender=UserQuizResponse)        
def delete_user_reward(sender, instance, **kwargs):
    # Buscar y borrar la recompensa relacionada si existe
    UserReward.objects.filter(user=instance.user, reward__quiz=instance.quiz).delete()
# models para sistema de recomendaciones 


#meses = [
#        [1, 'Enero'],
#        [2, 'Febrero'],
#        [3, 'Marzo'],
#        [4, 'Abril'],
#        [5, 'Mayo'],
#        [6, 'Junio'],
#        [7, 'Julio'],
#        [8, 'Agosto'],
#        [9, 'Septiembre'],
#        [10, 'Octubre'],
#        [11, 'Noviembre'],
#        [12, 'Diciembre'],
#    ]
#
#dias = [
#    [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'], 
#    [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10'], 
#    [11, '11'], [12, '12'], [13, '13'], [14, '14'], [15, '15'], 
#    [16, '16'], [17, '17'], [18, '18'], [19, '19'], [20, '20'], 
#    [21, '21'], [22, '22'], [23, '23'], [24, '24'], [25, '25'], 
#    [26, '26'], [27, '27'], [28, '28'], [29, '29'], [30, '30'], 
#    [31, '31']
#]
#
#class Books(models.Model):
#    years = [(year, str(year)) for year in range(1000, date.today().year + 1)]
#    #decir que tipo de dato estamos introduciendo 
#    title = models.CharField(max_length=200) #CharField para strings o textos pequeños
#    author = models.CharField(max_length=30)
#    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books")
#    subgenre = models.ManyToManyField(Subgenre, related_name='books')
#    description = models.TextField #TextField para textos largos
#    year = models.IntegerField(choices=years, null=True, blank=True)
#    month = models.IntegerField(choices= meses, null=True, blank=True)
#    day = models.IntegerField(choices= dias, null=True, blank=True)
#    cover_image = models.ImageField(upload_to="imagenes", null=True)
#
#    
#    def __str__(self):
#        return self.title
#    
#    def get_subgenres(self):
#        return ", ".join([sub.name for sub in self.subgenre.all()])  # Crea una cadena con los nombres de los subgéneros
#
#    get_subgenres.short_description = 'get_subgenres'  # Nombre de la columna en el admin
#