from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
# Create your models here.

class Author(models.Model):
    name=models.CharField(verbose_name="Author Name" , max_length=255)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='books')  # Related to Author
    publisher = models.CharField(max_length=100)
    publication_year = models.DateField(max_length=4)
    isbn = models.CharField(max_length=25,unique=True)
    genre = models.CharField(max_length=50,default="",null=True,blank=True)
    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="favorites")
    books = models.ManyToManyField(Book, blank=True)