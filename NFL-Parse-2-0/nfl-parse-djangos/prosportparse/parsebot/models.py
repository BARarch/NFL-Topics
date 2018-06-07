from django.db import models

# Create your models here.

class Article(models.Model):
	date = models.CharField(max_length=120)
	team = models.CharField(max_length=120)
	title = models.TextField()
	newsType = models.CharField(max_length=120)
	link = models.TextField()
	discription = models.TextField()
	creator = models.CharField(max_length=120)
	new = models.BooleanField()
	visited = models.BooleanField()

