from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Collection(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)

  def __str__(self):
    return f"{self.title}"


class Tag(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return f"{self.name}"

class Photo(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
  archive = models.CharField(max_length=300)
  isFavorite = models.BooleanField(default=False)
  created_date = models.DateTimeField(default=timezone.now)
  tags = models.ManyToManyField(Tag)