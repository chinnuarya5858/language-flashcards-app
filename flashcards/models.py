from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flashcard(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    LANGUAGE_CHOICES=[
        ('EN','English'),
        ('ES','Spanish'),
        ('FR','French'),
        ('DE','German'),
    ]
    word=models.CharField(max_length=255)
    meaning=models.TextField()
    example_sentences=models.TextField(blank=True,null=True)
    language=models.CharField(max_length=2,choices=LANGUAGE_CHOICES)
    difficulty=models.IntegerField(default=1)#1=Easy,2=Medium,3=Hard
    last_reviewed=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word
